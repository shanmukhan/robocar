#!/usr/bin/env python3
"""Regenerate individual print meshes, placed components, and visual assembly."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fingerprints(paths):
    return {str(p): sha256(p) for p in paths}


def render(job, binary, stage, timeout):
    started = time.monotonic()
    staged_outputs = [stage / f'{job["id"]}_{p.name}' for p in job["outputs"]]
    staged_summary = stage / f'{job["id"]}.summary.json'
    command = [binary, "--backend=Manifold"]
    for path in staged_outputs:
        command.extend(["-o", str(path)])
    command.extend(["--summary=all", f"--summary-file={staged_summary}"])
    if any(p.suffix == ".png" for p in job["outputs"]):
        command.extend([
            "--imgsize=1800,1400", "--camera=-260,-300,220,0,0,20",
            "--projection=o", "--viewall", "--autocenter", "--render=1",
            "--colorscheme=Tomorrow",
        ])
    command.append(str(job["source"]))
    try:
        run = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, timeout=timeout)
        output, returncode = run.stdout, run.returncode
    except subprocess.TimeoutExpired as error:
        output = error.stdout or ""
        if isinstance(output, bytes):
            output = output.decode(errors="replace")
        output += f"\nERROR: Render exceeded {timeout} seconds.\n"
        returncode = -1
    except OSError as error:
        output, returncode = f"ERROR: {error}\n", -1
    staged_log = stage / f'{job["id"]}.log'
    staged_log.write_text(output)
    diagnostics = re.findall(r"(?im)^.*(?:\bERROR:|\bWARNING:|Can't open file|not found|not a valid 2-manifold).*$", output)
    missing = [str(final) for staged, final in zip(staged_outputs, job["outputs"])
               if not staged.exists() or staged.stat().st_size == 0]
    try:
        summary = json.loads(staged_summary.read_text())
    except (OSError, ValueError):
        summary = None
    failed = bool(returncode or diagnostics or missing or summary is None)
    result = {
        "id": job["id"], "role": job["role"],
        "source": str(job["source"]), "source_sha256": sha256(job["source"]),
        "command": command, "returncode": returncode,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "diagnostics": diagnostics, "missing_or_empty_outputs": missing,
        "summary_valid": summary is not None, "summary": summary,
        "success": not failed,
        "artifacts": [{"path": str(final), "sha256": sha256(staged),
                       "bytes": staged.stat().st_size}
                      for staged, final in zip(staged_outputs, job["outputs"])
                      if staged.exists()],
        "log": str(job["log"]), "summary_file": str(job["summary"]),
    }
    if "component_index" in job:
        result["component_index"] = job["component_index"]
    return job, result, list(zip(staged_outputs, job["outputs"])) + [
        (staged_log, job["log"]), (staged_summary, job["summary"])]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--openscad", default=os.environ.get("OPENSCAD_BIN"),
                        help="OpenSCAD executable; defaults to OPENSCAD_BIN")
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--jobs", type=int, choices=[1, 2, 3], default=3)
    parser.add_argument("--components", type=int, default=27)
    parser.add_argument("--part-previews", action="store_true", help="Also render every printable part PNG")
    parser.add_argument("--timeout", type=int, default=300, help="Seconds per export job")
    args = parser.parse_args()
    if not args.openscad:
        parser.error("Pass --openscad or set OPENSCAD_BIN to a working OpenSCAD executable")
    resolved_binary = shutil.which(args.openscad)
    if resolved_binary is None:
        parser.error(f"OpenSCAD executable not found: {args.openscad}")
    binary = str(Path(resolved_binary).resolve())
    root = args.source_root.resolve()
    audit, exports = root / "audit", root / "exports"
    logs, components = audit / "render_logs", audit / "components"
    for directory in [exports, logs, components]:
        directory.mkdir(parents=True, exist_ok=True)
    master = root / "cute_rover_complete.scad"
    wrappers = sorted(p for p in (root / "parts").glob("*.scad") if p.stem != "assembly")
    if not master.is_file() or not wrappers:
        parser.error("Source root must contain cute_rover_complete.scad and printable parts/*.scad")
    version_run = subprocess.run([binary, "--version"], text=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, timeout=30)
    if version_run.returncode or "OpenSCAD version" not in version_run.stdout:
        parser.error(f"OpenSCAD version probe failed: {version_run.stdout.strip()}")
    before = fingerprints([master] + wrappers)
    jobs = []
    for wrapper in wrappers:
        name = wrapper.stem
        jobs.append({"id": name, "role": "printable_component", "source": wrapper,
                     "outputs": [exports / f"{name}.stl", exports / f"{name}.csg"]+([exports / f"{name}.png"] if args.part_previews else []),
                     "log": logs / f"{name}.log", "summary": logs / f"{name}.summary.json"})
    for index in range(args.components):
        name = f"component_{index:02d}"
        wrapper = components / f"{name}.scad"
        wrapper.write_text(f"// Generated placed component, units mm; not a print orientation.\n$fn=96;\nuse <{master}>;\nassembly_component({index});\n")
        jobs.append({"id": name, "role": "placed_assembly_component", "source": wrapper,
                     "component_index": index, "outputs": [components / f"{name}.stl"],
                     "log": logs / f"{name}.log", "summary": logs / f"{name}.summary.json"})
    jobs.append({"id": "visual_assembly", "role": "visual_only_assembly_not_for_printing",
                 "source": master,
                 "outputs": [root / "cute_rover_complete.stl", root / "cute_rover_complete.csg",
                             root / "cute_rover_assembled_preview.png"],
                 "log": logs / "visual_assembly.log", "summary": logs / "visual_assembly.summary.json"})
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "openscad_executable": binary, "openscad_version": version_run.stdout.strip(),
        "source_root": str(root), "source_sha256": before,
        "printable_parts": len(wrappers), "placed_components": args.components,
        "assembly_warning": "Complete assembly STL is visual-only: it includes hardware envelopes and assembled touching surfaces. Print only exports/*.stl after reading the audit and resolving hardware fit.",
        "jobs": [],
    }
    with tempfile.TemporaryDirectory(prefix=".export_cad_", dir=audit) as temp:
        stage = Path(temp)
        completed = []
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            futures = [executor.submit(render, job, binary, stage, args.timeout) for job in jobs]
            for future in as_completed(futures):
                job, result, copies = future.result()
                completed.append((job, result, copies))
                print(f'{job["id"]}: {"OK" if result["success"] else "FAILED"}', flush=True)
        manifest["jobs"] = sorted([record for _, record, _ in completed], key=lambda r: r["id"])
        after = fingerprints([master] + wrappers)
        manifest["source_unchanged_during_export"] = before == after
        manifest["success"] = before == after and all(r["success"] for r in manifest["jobs"])
        if not manifest["success"]:
            for _, _, copies in completed:
                for source, target in copies:
                    if source.suffix in [".log", ".json"] and source.exists():
                        shutil.copyfile(source, target)
            failed_path = audit / "export_manifest.last_failed.json"
            failed_path.write_text(json.dumps(manifest, indent=2) + "\n")
            print(f"Export failed; current exports preserved. Inspect {failed_path}", file=sys.stderr)
            return 1
        for _, _, copies in completed:
            for source, target in copies:
                source.replace(target)
        manifest_path = audit / "export_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        failed_path = audit / "export_manifest.last_failed.json"
        if failed_path.exists():
            failed_path.unlink()
        print(f"Exported {len(wrappers)} printable parts, {args.components} placed components, and visual assembly. Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Toolchain and baseline geometry evidence

Audit tooling was provisioned on 2026-10-09 without installing applications or packages system-wide. Downloads, app extraction and Python environment are under `/private/tmp`; these temporary paths may be removed by macOS.

- Host: macOS, Apple Silicon / `arm64`.
- OpenSCAD executable: `/private/tmp/cute-OpenSCAD.app/Contents/MacOS/OpenSCAD`.
- OpenSCAD version: **2026.10.08**, universal `arm64` / `x86_64` binary.
- Download: [official OpenSCAD snapshot](https://files.openscad.org/snapshots/OpenSCAD-2026.10.08.dmg).
- Official `.sha256` checksum file was fetched separately; `shasum -a 256 -c OpenSCAD-2026.10.08.dmg.sha256` returned `OK`.
- The DMG was mounted read-only at `/private/tmp/cute-openscad-mount`, copied with `ditto` to the temporary app path, then unmounted.
- Python environment: `/private/tmp/cute-cad-venv/bin/python`, Python 3.13. Installed dependencies: trimesh **5.1.1**, manifold3d **3.5.4**, numpy **2.5.3**, scipy **1.18.1**, Pillow **12.3.0**, matplotlib **3.11.2**.

## Running OpenSCAD

The restricted execution sandbox prevents Qt from detecting the host's NEON CPU feature. The same verified binary runs successfully with the approved execution escalation; no system setting was changed. All CAD export invocations used that approval.

Use absolute input and output paths. This snapshot changes its working directory between multiple `-o` exports: a relative first STL path works, but a relative second CSG path fails while the process still returns exit status 0. Final baseline exports all used absolute paths and produced both files.

```sh
/private/tmp/cute-OpenSCAD.app/Contents/MacOS/OpenSCAD \
  -o /absolute/output/part.stl \
  -o /absolute/output/part.csg \
  --summary=all --summary-file=/absolute/output/part.summary.json \
  /absolute/input/part.scad > /absolute/output/part.log 2>&1
```

STL export performs full geometry evaluation. For an evaluated PNG add `-o /absolute/output/part.png --imgsize=1400,1000 --viewall --autocenter --render=1`. This snapshot requires a value for `--render`; a bare flag consumes the next argument.

## Baseline evidence

`baseline_meshes/` contains STL, CSG, OpenSCAD summaries and logs for every preserved baseline wrapper. Empty final logs signify no warnings or errors; structured render evidence is in the adjacent summary JSON.

`baseline_mesh_metrics.json` inspects those 12 STLs and the preserved pre-existing assembly STL. `mesh_metrics.py` preserves STL coordinates and welds vertices only when they are exactly equal. It does not repair topology or normals. It reports face counts, bounds, connected components, signed volume, winding, exact edge incidences, duplicate/degenerate faces and independent manifold3d import status. STL has no unit metadata; millimetres follow the corresponding source.

The 12 source-generated baseline wrappers have closed, consistently wound meshes, but mesh validity alone does not establish mechanical or printing readiness. The adapter contains two disconnected solids. The preserved old complete STL has one edge with four incident faces, so its exactly welded topology is non-manifold. manifold3d nevertheless imports it with `NoError`; that status does not override the explicit edge incidence result.

## Wrapper tessellation mismatch

The preserved master's global `$fn=48` assignment is not imported by a `use <...>` wrapper. Baseline wrapper CSG primitives show `$fn=0, $fa=12, $fs=2`, using the OpenSCAD automatic fragment count rather than 48. In particular, a 3.2 mm cylinder uses the minimum five fragments; its geometric fit differs from a 48-fragment hole.

`baseline_meshes/fn_comparison/` and `baseline_fn_comparison.json` demonstrate the difference without changing source:

| Export | Baseline wrapper faces | Master / forced `$fn=48` faces |
| --- | ---: | ---: |
| Complete assembly | 5,692 | 18,870 |
| Base plate | 436 | 3,084 |
| Wheel | 544 | 912 |

The old preserved STL also differs substantially from current preserved source geometry: old bounds span **227.4263 × 172.5 × 48.9263 mm**; both baseline source assembly exports span **150 × 138 × 48 mm**. It is a stale export, not an individual print layout or trustworthy current assembly export.

Re-run mesh inspection from the repository root:

```sh
/private/tmp/cute-cad-venv/bin/python \
  01_Cute_N20_4WD/audit/tooling/mesh_metrics.py \
  01_Cute_N20_4WD/audit/baseline_meshes/*.stl \
  01_Cute_N20_4WD/audit/baseline/cute_rover_complete.stl \
  --output 01_Cute_N20_4WD/audit/baseline_mesh_metrics.json
```

Self-intersection, hardware fit, assembly insertion, minimum wall thickness, overhangs and manufacturing tolerances require separate checks; numerical topology metrics do not certify these properties.

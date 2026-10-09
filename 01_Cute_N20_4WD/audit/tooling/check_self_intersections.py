#!/usr/bin/env python3
"""Independently inspect printable STL triangle crossings without mesh repair."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import trimesh


class Node:
    def __init__(self, ids, lower, upper, centres):
        self.lower = lower[ids].min(axis=0)
        self.upper = upper[ids].max(axis=0)
        self.count = len(ids)
        self.left = self.right = None
        self.ids = ids
        if len(ids) > 8:
            axis = np.argmax(np.ptp(centres[ids], axis=0))
            ordered = ids[np.argsort(centres[ids, axis], kind="stable")]
            middle = len(ids) // 2
            self.left = Node(ordered[:middle], lower, upper, centres)
            self.right = Node(ordered[middle:], lower, upper, centres)
            self.ids = None


def candidates(root, lower, upper, eps):
    stack = [(root, root)]
    while stack:
        a, b = stack.pop()
        if np.any(a.lower > b.upper + eps) or np.any(b.lower > a.upper + eps):
            continue
        if a is b:
            if a.ids is None:
                stack.extend([(a.left, a.left), (a.left, a.right), (a.right, a.right)])
                continue
            first, second = np.triu_indices(len(a.ids), 1)
            i, j = a.ids[first], a.ids[second]
        elif a.ids is not None and b.ids is not None:
            i = np.repeat(a.ids, len(b.ids))
            j = np.tile(b.ids, len(a.ids))
        elif b.ids is not None or (a.ids is None and a.count >= b.count):
            stack.extend([(a.left, b), (a.right, b)])
            continue
        else:
            stack.extend([(a, b.left), (a, b.right)])
            continue
        mask = np.all(lower[i] <= upper[j] + eps, axis=1) & np.all(lower[j] <= upper[i] + eps, axis=1)
        yield from zip(i[mask], j[mask])


def cross2(a, b):
    return a[0] * b[1] - a[1] * b[0]


def clipped_coplanar_polygon(first, second, normal):
    drop = int(np.argmax(np.abs(normal)))
    axes = [a for a in range(3) if a != drop]
    polygon = [p[axes] for p in first]
    clip = second[:, axes]
    if cross2(clip[1] - clip[0], clip[2] - clip[0]) < 0:
        clip = clip[::-1]
    for index in range(3):
        start, end = clip[index], clip[(index + 1) % 3]
        edge = end - start
        previous = polygon[-1] if polygon else None
        result = []
        for current in polygon:
            d_current = cross2(edge, current - start)
            d_previous = cross2(edge, previous - start)
            current_inside, previous_inside = d_current >= 0, d_previous >= 0
            if current_inside != previous_inside:
                fraction = d_previous / (d_previous - d_current)
                result.append(previous + fraction * (current - previous))
            if current_inside:
                result.append(current)
            previous = current
        polygon = result
        if not polygon:
            break
    return polygon


def plane_interval(triangle, distances, axis, eps):
    points = [triangle[i] for i in range(3) if abs(distances[i]) <= eps]
    for i in range(3):
        j = (i + 1) % 3
        if (distances[i] < -eps and distances[j] > eps) or (distances[j] < -eps and distances[i] > eps):
            fraction = distances[i] / (distances[i] - distances[j])
            points.append(triangle[i] + fraction * (triangle[j] - triangle[i]))
    if not points:
        return None
    projected = np.asarray(points) @ axis
    return float(projected.min()), float(projected.max())


def classify(first, second, normal_first, normal_second, shared, eps):
    distances_second = (second - first[0]) @ normal_first
    distances_first = (first - second[0]) @ normal_second
    if np.all(distances_second > eps) or np.all(distances_second < -eps):
        return None
    if np.all(distances_first > eps) or np.all(distances_first < -eps):
        return None
    if np.max(np.abs(distances_first)) <= eps and np.max(np.abs(distances_second)) <= eps:
        polygon = clipped_coplanar_polygon(first, second, normal_first)
        if len(polygon) < 3:
            return None
        area = abs(sum(cross2(polygon[i], polygon[(i + 1) % len(polygon)]) for i in range(len(polygon)))) / 2
        characteristic = max(np.ptp(first, axis=0).max(), np.ptp(second, axis=0).max(), eps)
        if area > eps * characteristic:
            return {"type": "coplanar_area_overlap", "projected_overlap_area_mm2": float(area),
                    "area_detection_threshold_mm2": float(eps * characteristic)}
        return None
    axis = np.cross(normal_first, normal_second)
    norm = np.linalg.norm(axis)
    if norm < 1e-12:
        return None
    axis /= norm
    interval_first = plane_interval(first, distances_first, axis, eps)
    interval_second = plane_interval(second, distances_second, axis, eps)
    if interval_first is None or interval_second is None:
        return None
    low = max(interval_first[0], interval_second[0])
    high = min(interval_first[1], interval_second[1])
    if high - low <= eps:
        return None
    if len(shared) >= 2:
        common = shared @ axis
        if low >= common.min() - eps and high <= common.max() + eps:
            return None  # The expected common mesh edge, not a crossing.
    return {"type": "transverse_segment_intersection", "intersection_length_mm": float(high - low)}


def inspect_mesh(raw, eps):
    started = time.monotonic()
    vertices, inverse = np.unique(raw.vertices, axis=0, return_inverse=True)
    faces = inverse[raw.faces]
    triangles = vertices[faces]
    lower, upper = triangles.min(axis=1), triangles.max(axis=1)
    normals = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    lengths = np.linalg.norm(normals, axis=1)
    degenerate = lengths == 0
    normals[~degenerate] /= lengths[~degenerate, None]
    tree = Node(np.arange(len(faces)), lower, upper, (lower + upper) / 2)
    pair_count = intersections = coplanar = transverse = adjacent = 0
    examples = []
    for first_id, second_id in candidates(tree, lower, upper, eps):
        pair_count += 1
        if degenerate[first_id] or degenerate[second_id]:
            continue
        first, second = triangles[first_id], triangles[second_id]
        common_ids = faces[first_id][np.any(faces[first_id][:, None] == faces[second_id][None, :], axis=1)]
        if len(common_ids):
            adjacent += 1
        result = classify(first, second, normals[first_id], normals[second_id], vertices[common_ids], eps)
        if result:
            intersections += 1
            coplanar += result["type"] == "coplanar_area_overlap"
            transverse += result["type"] == "transverse_segment_intersection"
            if len(examples) < 25:
                examples.append({"triangle_ids": [int(first_id), int(second_id)],
                                 "triangles_mm": [first.tolist(), second.tolist()],
                                 "shared_exact_vertices": len(common_ids), **result})
    return {"triangles": len(faces), "candidate_triangle_pairs": pair_count,
            "pairs_with_shared_exact_vertices": adjacent,
            "degenerate_triangles": int(degenerate.sum()),
            "finite_coordinates": bool(np.isfinite(vertices).all()),
            "detected_intersection_pairs": intersections,
            "coplanar_overlap_pairs": int(coplanar), "transverse_crossing_pairs": int(transverse),
            "examples_first_25": examples, "elapsed_seconds": round(time.monotonic() - started, 3)}


def inspect_path(path, eps):
    path = Path(path)
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    result = inspect_mesh(trimesh.load_mesh(path, process=False), eps)
    after = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"path": str(path.resolve()), "sha256": before,
            "unchanged_during_check": before == after, **result}


def controls(eps):
    first = trimesh.creation.box([10, 10, 10])
    overlapping = first.copy()
    overlapping.apply_translation([9, 0.25, 0.25])
    separated = first.copy()
    separated.apply_translation([10.1, 0.25, 0.25])
    coplanar_overlap = first.copy()
    coplanar_overlap.apply_translation([9, 0, 0])
    positive = inspect_mesh(trimesh.util.concatenate([first, overlapping]), eps)
    negative = inspect_mesh(trimesh.util.concatenate([first, separated]), eps)
    flat_overlap = inspect_mesh(trimesh.util.concatenate([first, coplanar_overlap]), eps)
    return {"purpose": "Mechanically relevant detection controls: two 10 mm solids overlapping by 1 mm with offset faces, two with aligned coplanar faces overlapping by 1 mm, and two separated by 0.1 mm. These synthetic controls do not modify project meshes.",
            "overlapping_boxes": positive, "coplanar_overlap_boxes": flat_overlap,
            "separated_boxes": negative,
            "passed": positive["transverse_crossing_pairs"] > 0 and flat_overlap["coplanar_overlap_pairs"] > 0 and negative["detected_intersection_pairs"] == 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("meshes", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--epsilon-mm", type=float, default=1e-8)
    parser.add_argument("--jobs", type=int, choices=[1, 2, 3], default=3)
    args = parser.parse_args()
    if any(p.name == "cute_rover_complete.stl" or p.stem == "assembly" for p in args.meshes):
        parser.error("Complete assembled STL is visual-only and cannot be included as a printable component")
    if args.epsilon_mm <= 0:
        parser.error("epsilon-mm must be positive")
    control = controls(args.epsilon_mm)
    records = []
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(inspect_path, path, args.epsilon_mm) for path in args.meshes]
        for future in as_completed(futures):
            result = future.result()
            records.append(result)
            print(f'{Path(result["path"]).name}: crossings={result["detected_intersection_pairs"]}, pairs={result["candidate_triangle_pairs"]}, seconds={result["elapsed_seconds"]}', flush=True)
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "method": "Independent float64 triangle-level inspection: BVH/AABB broad phase; mutual plane/line interval overlap for transverse crossings; projected convex polygon clipping for coplanar positive-area overlap. Exact-equal vertices are indexed together without changing coordinates. Shared-edge intersections are excluded only when limited to their expected common edge. Shared-vertex pairs remain checked for overlap beyond their common vertex. No repair, mesh simplification, approximate welding, or normal correction is performed.",
        "epsilon_mm": args.epsilon_mm,
        "scope": "Individual exports/*.stl printable meshes only; complete assembled STL is visual-only and excluded.",
        "limitations": "Numerical diagnostic, not an exact-predicate CGAL certificate. Positive-length crossings <= epsilon, coplanar overlap areas <= epsilon times the larger triangle extent, isolated point/edge contacts, and near-parallel normals below 1e-12 may remain unreported. ASCII STL rounding is preserved. Separate topology/normal checks, hardware interference checks and manufacturing review remain necessary.",
        "reference_definition": "https://doc.cgal.org/latest/Polygon_mesh_processing/group__PMP__intersection__grp.html",
        "numpy_version": np.__version__, "trimesh_version": trimesh.__version__,
        "controls": control, "meshes": sorted(records, key=lambda r: r["path"]),
    }
    report["passed"] = control["passed"] and all(
        r["unchanged_during_check"] and r["finite_coordinates"] and not r["degenerate_triangles"] and not r["detected_intersection_pairs"]
        for r in records)
    manifest_path = args.output.parent / "export_manifest.json"
    if manifest_path.exists():
        manifest_bytes = manifest_path.read_bytes()
        manifest = json.loads(manifest_bytes)
        known_hashes = {a["path"]: a["sha256"] for job in manifest["jobs"] for a in job["artifacts"]}
        matches = all(known_hashes.get(r["path"]) == r["sha256"] for r in records)
        report["export_provenance"] = {
            "manifest_path": str(manifest_path.resolve()),
            "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "source_sha256": manifest["source_sha256"],
            "all_checked_meshes_match_successful_export_manifest": bool(matches and manifest["success"]),
        }
        report["passed"] = report["passed"] and matches and manifest["success"]
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(f'Printable mesh crossing diagnostic {"PASSED" if report["passed"] else "FAILED"}: {args.output}')
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

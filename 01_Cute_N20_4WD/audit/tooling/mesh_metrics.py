#!/usr/bin/env python3
"""Inspect STL topology without repairing it; export numerical audit evidence."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path

import manifold3d
import numpy as np
import trimesh


def inspect(path):
    path = Path(path)
    raw = trimesh.load_mesh(path, process=False)
    vertices, inverse = np.unique(raw.vertices, axis=0, return_inverse=True)
    faces = inverse[raw.faces]
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    edges = np.sort(mesh.edges, axis=1)
    unique_edges, edge_counts = np.unique(edges, axis=0, return_counts=True)
    canonical_faces = np.sort(faces, axis=1)
    _, face_counts = np.unique(canonical_faces, axis=0, return_counts=True)
    areas = trimesh.triangles.area(mesh.triangles)
    components = mesh.split(only_watertight=False)
    imported = manifold3d.Manifold(manifold3d.Mesh64(
        vert_properties=np.ascontiguousarray(vertices, dtype=np.float64),
        tri_verts=np.ascontiguousarray(faces, dtype=np.uint64),
    ))
    result = {
        "path": str(path),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
        "triangles": len(faces),
        "raw_vertices": len(raw.vertices),
        "exact_welded_vertices": len(vertices),
        "bounds_mm": mesh.bounds.tolist(),
        "extents_mm": mesh.extents.tolist(),
        "watertight": bool(mesh.is_watertight),
        "winding_consistent": bool(mesh.is_winding_consistent),
        "is_volume": bool(mesh.is_volume),
        "signed_volume_mm3": float(mesh.volume),
        "positive_volume": bool(mesh.volume > 0),
        "surface_area_mm2": float(mesh.area),
        "connected_face_components": len(components),
        "connected_closed_positive_solids": sum(
            bool(c.is_watertight and c.is_winding_consistent and c.volume > 0)
            for c in components
        ),
        "components": [{
            "triangles": len(c.faces),
            "bounds_mm": c.bounds.tolist(),
            "watertight": bool(c.is_watertight),
            "winding_consistent": bool(c.is_winding_consistent),
            "signed_volume_mm3": float(c.volume),
        } for c in components],
        "exact_welded_edges": len(edge_counts),
        "boundary_edges_incidence_1": int(np.count_nonzero(edge_counts == 1)),
        "nonmanifold_edges_incidence_gt2": int(np.count_nonzero(edge_counts > 2)),
        "maximum_edge_incidence": int(edge_counts.max(initial=0)),
        "all_edges_have_two_faces": bool(np.all(edge_counts == 2)),
        "nonmanifold_edge_examples": [{
            "coordinates_mm": vertices[edge].tolist(),
            "incident_faces": int(count),
        } for edge, count in list(zip(unique_edges[edge_counts > 2], edge_counts[edge_counts > 2]))[:20]],
        "duplicate_faces_ignoring_winding": int(np.sum(face_counts - 1)),
        "zero_area_faces": int(np.count_nonzero(areas == 0)),
        "near_degenerate_faces_area_le_1e_12_mm2": int(np.count_nonzero(areas <= 1e-12)),
        "finite_vertex_coordinates": bool(np.isfinite(vertices).all()),
        "manifold3d_import_status": str(imported.status()),
        "manifold3d_import_empty": bool(imported.is_empty()),
        "manifold3d_import_triangles": int(imported.num_tri()),
        "manifold3d_import_volume_mm3": float(imported.volume()),
    }
    summary = path.with_suffix(".summary.json")
    if summary.exists():
        result["openscad_summary"] = json.loads(summary.read_text())
    csg = path.with_suffix(".csg")
    if csg.exists():
        result["csg_sha256"] = hashlib.sha256(csg.read_bytes()).hexdigest()
    log = path.with_suffix(".log")
    if log.exists():
        result["openscad_log"] = log.read_text()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("meshes", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = {
        "method": "STL coordinates preserved. Vertices welded only when coordinates are exactly equal. No repair, simplification, approximate welding, or normal correction applied before metrics. Units mm inferred from the corresponding OpenSCAD source; STL does not encode units.",
        "limitations": "Topology, winding and oriented-manifold import checks do not establish hardware fit, minimum wall thickness, print process capability, or absence of all geometric self-intersections. Connected components can include intentional separate assembly parts.",
        "versions": {name: importlib.metadata.version(name) for name in ["trimesh", "manifold3d", "numpy", "scipy"]},
        "meshes": [inspect(path) for path in args.meshes],
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    for mesh in result["meshes"]:
        print(f'{Path(mesh["path"]).name}: faces={mesh["triangles"]}, watertight={mesh["watertight"]}, winding={mesh["winding_consistent"]}, bodies={mesh["connected_closed_positive_solids"]}, import={mesh["manifold3d_import_status"]}, bounds={mesh["extents_mm"]}')


if __name__ == "__main__":
    main()

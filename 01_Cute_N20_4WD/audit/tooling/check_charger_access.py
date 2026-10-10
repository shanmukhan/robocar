#!/usr/bin/env python3
"""Check the charger, rear plug path, ties, fasteners and board lift in default CAD.

Independent dimensions describe the reserved spaces, not purchased hardware.
Run validate_cad.py first to verify source/export hashes and assembly geometry.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import trimesh

from validate_cad import NAMES, load_mesh, solid

ROOT = Path(__file__).resolve().parents[2]


def box(low, high):
    low, high = np.array(low, dtype=float), np.array(high, dtype=float)
    mesh = trimesh.creation.box(extents=high-low)
    mesh.apply_translation((low+high)/2)
    return mesh


def cylinder(x, y, bottom, height, diameter, sections=96):
    mesh = trimesh.creation.cylinder(radius=diameter/2, height=height, sections=sections)
    mesh.apply_translation([x, y, bottom+height/2])
    return mesh


def main():
    validation = json.loads((ROOT/'audit/validation_results.json').read_text())
    source_hash = hashlib.sha256((ROOT/'cute_rover_complete.scad').read_bytes()).hexdigest()
    if not validation['pass'] or validation['master_source_sha256'] != source_hash:
        raise SystemExit('Run validate_cad.py on the current successful exports first')
    meshes = [load_mesh(ROOT/'audit/components'/f'component_{i:02d}.stl') for i in range(len(NAMES))]
    solids = [solid(mesh) for mesh in meshes]
    checks = []

    def check(name, moving, obstacles=None):
        moving_solid = solid(moving)
        overlaps = []
        for i in range(len(meshes)) if obstacles is None else obstacles:
            if np.any(np.minimum(moving.bounds[1], meshes[i].bounds[1]) <=
                      np.maximum(moving.bounds[0], meshes[i].bounds[0])+1e-8):
                continue
            overlap = moving_solid ^ solids[i]
            overlaps.append({'part': NAMES[i], 'volume_mm3': abs(overlap.volume()),
                             'status': str(overlap.status())})
        passed = all(x['volume_mm3'] < 0.001 and x['status'] == 'Error.NoError' for x in overlaps)
        checks.append({'name': name, 'bounds_mm': moving.bounds.tolist(),
                       'tested_overlaps': overlaps, 'pass': passed})

    board = box([19.5, 23.5, 48], [58.5, 41.5, 54.3])
    check('Published 39x18x6.3 mm board envelope at edge seats', board)
    for distance in [0, 0.5, 1, 2, 5, 10, 20, 30]:
        plug = box([58.5+distance, 25.5, 46.5], [88.5+distance, 39.5, 54.5])
        check(f'Rear 14x8x30 mm plug reservation, insertion offset {distance} mm', plug)
    for dz in [0.25, 1, 5, 10, 30]:
        lifted = board.copy()
        lifted.apply_translation([0, 0, dz])
        check(f'Board vertical service lift {dz} mm after releasing ties', lifted)
    for x in [27, 51]:
        check(f'M3x10 shaft at ({x},28.5)', cylinder(x, 28.5, 34, 10, 3))
        check(f'M3 head at ({x},28.5)', cylinder(x, 28.5, 44, 3, 6.6))
        check(f'M3 tool access before installing PCB at ({x},28.5)',
              cylinder(x, 28.5, 44, 20, 6.6))
        # Hex nut below deck, 5.7 mm AF / 2.7 mm tall; no washer in this stack.
        nut = cylinder(x, 28.5, 35.3, 2.7, 2*5.7/np.sqrt(3), sections=6)
        check(f'M3 nut under deck at ({x},28.5)', nut)
        head = cylinder(x, 28.5, 44, 3, 6.6)
        overlap = abs((solid(head) ^ solid(board)).volume())
        checks.append({'name': f'M3 head vs board at X={x}', 'volume_mm3': overlap,
                       'vertical_clearance_mm': 1, 'pass': overlap < 0.001})
    for x in [33, 45]:
        for y in [19.6, 45.4]:
            check(f'Tie slot through floor ({x},{y})',
                  box([x-1.39, y-0.69, 40.9], [x+1.39, y+0.69, 44.1]), [27])
        check(f'Tie under-floor channel at X={x}, clear of installed deck',
              box([x-1.39, 18.91, 41.01], [x+1.39, 46.09, 42.39]))
    # Mechanically relevant negative control: a boot larger than the 14 mm notch
    # must hit the guard. This detects a missing/ignored mount in the checks.
    oversized_boot = solid(box([58.5, 23.5, 46.5], [88.5, 41.5, 54.5]))
    control_overlap = abs((oversized_boot ^ solids[27]).volume())
    checks.append({'name': 'Control: 18 mm wide boot collides with rear guard',
                   'volume_mm3': control_overlap, 'pass': control_overlap > 1})
    result = {'generated_at_utc': datetime.now(timezone.utc).isoformat(),
              'master_source_sha256': source_hash,
              'method': 'Independent default dimensions; manifold3d Boolean intersections against all 28 source-exported assembly components. Contact planes allowed; interference threshold 0.001 mm3.',
              'limitations': ['Board and plug are reserved bounding boxes; PCB underside, USB connector offset, solder pads, actual plug, cable bend and tie routes require measurement.',
                              'Electrical charge/protection/balancing and physical fit/strength are not certified by these geometric checks.',
                              'Fastener tool check assumes PCB is fitted after the carrier screws; actual hardware must match the modeled dimensions.'],
              'checks': checks, 'passed': all(item['pass'] for item in checks)}
    path = ROOT/'audit/charger_access_results.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(f"Charger: {len(checks)} checks; passed={result['passed']}")
    for item in checks:
        if not item['pass']:
            print('FAIL:', item['name'])
    return int(not result['passed'])


if __name__ == '__main__':
    raise SystemExit(main())

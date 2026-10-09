#!/usr/bin/env python3
"""Independent nominal hardware-envelope probes against a frozen source copy.

These checks cover printed material interference, not purchased hardware fit.
Run with the audit virtualenv and --openscad pointing at the renderer.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import warnings

import trimesh


PREAMBLE = r'''
$fn=96;
use <mechanical_source_snapshot.scad>;
module actual_nut() { cylinder(r=5.5/sqrt(3),h=2.4,$fn=6); }
module heads_and_tools(points,foot_h) {
    for(p=points) {
        translate([p[0],p[1],foot_h]) cylinder(d=6.6,h=3);
        translate([p[0],p[1],foot_h+3]) cylinder(d=8,h=30);
    }
}
module axial_hardware() {
    for(a=[90,210,330]) {
        p=[9*cos(a),9*sin(a)];
        translate([p[0],p[1],0.1]) actual_nut();
        translate([p[0],p[1],0]) cylinder(d=3,h=14);
        translate([p[0],p[1],14]) cylinder(d=6.6,h=3);
    }
}
module radial_hardware(a=30,tool=true) {
    rotate([0,0,a]) {
        translate([8.1,0,4.5]) rotate([0,90,0]) rotate([0,0,30]) actual_nut();
        translate([1.6,0,4.5]) rotate([0,90,0]) cylinder(d=3,h=10);
        if(tool) translate([11.6,0,4.5]) rotate([0,90,0]) cylinder(d=3,h=20);
    }
}
module placed_hub_shanks(length=14) {
    for(sx=[-1,1],sy=[-1,1]) axle_placement(sx,sy)
        for(a=[90,210,330])
            translate([9*cos(a),9*sin(a),14-length]) cylinder(d=3,h=length);
}
'''

CASES = {
    'camera_heads_tools': '''intersection() {
        camera_mount();
        heads_and_tools([[-2,-14],[-2,14],[8,-10],[8,10]],3);
    }''',
    'tof_heads_tools': '''intersection() {
        tof_sensor_bar();
        heads_and_tools([[11,-12],[11,12]],4);
    }''',
    'bumper_heads_tools': '''intersection() {
        front_bumper();
        heads_and_tools([[16,0],[24,0]],3);
    }''',
    'motor_heads_allen_tools': '''intersection() {
        n20_motor_mount();
        union() for(x=[-12,12]) {
            translate([x,-15.5,3]) cylinder(d=6.6,h=3);
            translate([x,-15.5,6]) cylinder(d=3,h=30);
        }
    }''',
    'hub_hardware_printed_material': '''intersection() {
        union() { wheel(); wheel_hub_adapter(); }
        union() { axial_hardware(); radial_hardware(); }
    }''',
    'hub_radial_vs_axial_hardware': '''intersection() {
        axial_hardware(); radial_hardware(30,false);
    }''',
    'flush_hub_bolts_vs_saddles': '''intersection() {
        union() for(i=[1:4]) assembly_component(i);
        placed_hub_shanks(14);
    }''',
    'control_bad_radial_angle_zero': '''intersection() {
        axial_hardware(); radial_hardware(0,false);
    }''',
    'control_unspaced_m3x16_vs_saddles': '''intersection() {
        union() for(i=[1:4]) assembly_component(i);
        placed_hub_shanks(16);
    }''',
}


def probe(name,body,directory,binary):
    scad=directory/f'{name}.scad'
    stl=directory/f'{name}.stl'
    stl.unlink(missing_ok=True)
    scad.write_text(PREAMBLE+body+'\n')
    command=[binary,'--backend=Manifold','-o',str(stl),str(scad)]
    run=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                       text=True,timeout=60)
    log=directory/f'{name}.log'
    log.write_text(run.stdout)
    result={'name':name,'command':command,'returncode':run.returncode,
            'log':str(log),'source':str(scad)}
    diagnostics=re.findall(r'(?im)^.*(?:\bERROR:|\bWARNING:|Incompatible processor|not a valid 2-manifold).*$'
                           ,run.stdout)
    expected_empty=('Current top level object is empty' in run.stdout)
    result.update(diagnostics=diagnostics,
                  renderer_ok=bool(not diagnostics and (run.returncode==0 or
                                   (run.returncode==1 and expected_empty))))
    if stl.exists() and stl.stat().st_size:
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore',category=RuntimeWarning,module=r'trimesh\.triangles')
            mesh=trimesh.load_mesh(stl,process=True)
            volume=float(mesh.volume)
        result.update(empty=False,intersection_volume_mm3=volume,
                      positive_volume_collision=bool(abs(volume)>1e-8),
                      bounds_mm=mesh.bounds.tolist(),watertight=bool(mesh.is_watertight))
    elif expected_empty and result['renderer_ok']:
        result.update(empty=True,intersection_volume_mm3=0.0,positive_volume_collision=False)
    else:
        result.update(empty=None,error=run.stdout)
    expected_collision=name.startswith('control_')
    result.update(expected_positive_collision=expected_collision,
                  passed=bool(result['renderer_ok'] and
                              result.get('positive_volume_collision')==expected_collision))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--openscad',required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[2]
    source=root/'cute_rover_complete.scad'
    directory=root/'audit'/'hardware_checks'
    directory.mkdir(exist_ok=True)
    data=source.read_bytes()
    (directory/'mechanical_source_snapshot.scad').write_bytes(data)
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures=[executor.submit(probe,n,b,directory,args.openscad) for n,b in CASES.items()]
        results=[f.result() for f in futures]
    report={
        'generated_at_utc':datetime.now(timezone.utc).isoformat(),
        'source_sha256':hashlib.sha256(data).hexdigest(),
        'source_changed_during_checks':source.read_bytes()!=data,
        'method':'OpenSCAD Manifold solid intersections against an untouched source snapshot.',
        'assumptions':[
            'M3 nut AF5.5, thickness2.4 in CAD pockets AF5.7/thickness2.7.',
            'Conservative head diameter6.6, height3; socket access cylinder diameter8 for front carriers.',
            'Motor heads use diameter3 Allen-tool envelope above the head; nuts must be below the base.',
            'Radial hub fastener must be a headless M3 grub screw; diameter3, nominal10mm length.',
            'Axial hub bolts have14mm effective under-head length and flush inboard tips; M3x16 requires2mm head-side spacers.',
            'Radial Allen-tool envelope diameter3; wheel/hub assembled at matching angle30 degrees.',
            'No purchased component dimensional certification, physical wrench fit, thread strength or optical FOV certification.',
        ],
        'expected':'No positive-volume intersections above1e-8mm3 except intentional bad-angle and unspaced-M3x16 controls. Face contacts at intended seating planes can produce zero-volume sheets; these are probe artefacts, not printable solids.',
        'results':results,
    }
    report['passed']=bool(not report['source_changed_during_checks'] and
                          len(results)==9 and all(r['passed'] for r in results))
    (directory/'nominal_hardware_results.json').write_text(json.dumps(report,indent=2)+'\n')
    for result in results:
        print(result['name'],result.get('intersection_volume_mm3',result.get('error')))
    print('Hardware access probes passed:',report['passed'])
    if not report['passed']:
        raise SystemExit(1)


if __name__=='__main__':
    main()

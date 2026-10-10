#!/usr/bin/env python3
"""Validate unrepaired meshes, placed-part equivalence and solid interferences."""
import argparse, hashlib, importlib.metadata, itertools, json, sys
from pathlib import Path
import numpy as np
import trimesh
import manifold3d as m
from mesh_metrics import inspect
PROJECT=Path(__file__).resolve().parents[2]
NAMES=['base']+[f'mount_{i}' for i in range(4)]+[f'motor_envelope_{i}' for i in range(4)]+[f'wheel_{i}' for i in range(4)]+[f'hub_{i}' for i in range(4)]+['battery','deck']+[f'standoff_{i}' for i in range(4)]+['esp_carrier','camera','tof','bumper','usb_c_charger_mount']
EXPECTED_SOLIDS={'standoffs':4}
LOCAL_FOR_INDEX={0:'base_plate',17:'battery_tray',18:'top_cover',23:'esp32_tray',24:'camera_mount',25:'tof_sensor_bar',26:'front_bumper',27:'usb_c_charger_mount'}
LOCAL_FOR_INDEX.update({i:'n20_motor_mount' for i in range(1,5)})
LOCAL_FOR_INDEX.update({i:'wheel' for i in range(9,13)})
LOCAL_FOR_INDEX.update({i:'wheel_hub_adapter' for i in range(13,17)})
def load_mesh(p):
    raw=trimesh.load_mesh(p,process=False)
    v,inv=np.unique(raw.vertices,axis=0,return_inverse=True)
    return trimesh.Trimesh(vertices=v,faces=inv[raw.faces],process=False)
def solid(mesh):
    return m.Manifold(m.Mesh64(vert_properties=np.ascontiguousarray(mesh.vertices,dtype=np.float64),tri_verts=np.ascontiguousarray(mesh.faces,dtype=np.uint64)))
def matrix(i):
    a=np.eye(4)
    if 1<=i<=16:
        sx=-1 if (i-1)%2==0 else 1; sy=-1 if ((i-1)%4)//2==0 else 1
        if i<=8:
            a[1,1]=sy;a[:3,3]=[sx*52,sy*52.5,4]
        else:
            a[:3,:3]=[[1,0,0],[0,0,sy],[0,-sy,0]]
            a[:3,3]=[sx*52,sy*54.5,17.5]
    elif i==17:a[:3,3]=[0,0,4]
    elif i==18:a[:3,3]=[0,0,38]
    elif 19<=i<=22:a[:3,3]=[[-50,-14],[-50,14],[50,-14],[50,14]][i-19]+[4]
    elif i==23:a[:3,3]=[16,0,41]
    elif i==24:a[:3,3]=[-48,0,41]
    elif i==25:a[:3,3]=[-80,0,4]
    elif i==26:a[:3,3]=[-87,0,4]
    elif i==27:a[:3,3]=[39,32.5,41]
    return a

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,default=PROJECT/'audit'/'validation_results.json');args=ap.parse_args()
    failures=[]
    manifest=json.loads((PROJECT/'audit'/'export_manifest.json').read_text())
    if not manifest.get('success'):failures.append('Export manifest is not successful')
    for source,expected_hash in manifest['source_sha256'].items():
        path=Path(source)
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected_hash:
            failures.append(f'Source changed after exports: {path.name}')
    for job in manifest['jobs']:
        for artifact in job['artifacts']:
            path=Path(artifact['path'])
            if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=artifact['sha256']:
                failures.append(f'Export hash mismatch: {path.name}')
    parts=[]
    for p in sorted((PROJECT/'exports').glob('*.stl')):
        if p.stem=='assembly':continue
        r=inspect(p);r['path']=str(p.relative_to(PROJECT))
        expected=EXPECTED_SOLIDS.get(p.stem,1)
        ok=(r['watertight'] and r['winding_consistent'] and r['is_volume'] and r['all_edges_have_two_faces'] and r['zero_area_faces']==0 and r['duplicate_faces_ignoring_winding']==0 and r['finite_vertex_coordinates'] and r['connected_closed_positive_solids']==expected and abs(r['bounds_mm'][0][2])<1e-6 and r['manifold3d_import_status']=='Error.NoError')
        r['expected_solids']=expected;r['pass']=bool(ok)
        if not ok:failures.append(f'Printable topology/origin failed: {p.stem}')
        parts.append(r)
    # Missing exports must not make a vacuous pass.
    required={p.stem for p in (PROJECT/'parts').glob('*.scad') if p.stem!='assembly'}
    found={Path(p['path']).stem for p in parts}
    if required!=found:failures.append(f'Export set mismatch: required={sorted(required)}, found={sorted(found)}')
    placed=[];solids=[];component_reports=[]
    for i in range(len(NAMES)):
        p=PROJECT/'audit'/'components'/f'component_{i:02d}.stl'
        mesh=load_mesh(p);placed.append(mesh);solids.append(solid(mesh))
        rr=inspect(p);rr['path']=str(p.relative_to(PROJECT));rr['name']=NAMES[i]
        if not rr['watertight'] or not rr['all_edges_have_two_faces']:failures.append(f'Placed component invalid: {NAMES[i]}')
        component_reports.append(rr)
    equivalence=[]
    for i in sorted(LOCAL_FOR_INDEX):
        loc=load_mesh(PROJECT/'exports'/f'{LOCAL_FOR_INDEX[i]}.stl')
        if 9<=i<=12:
            # Export wheel_print() flips axial orientation to open pocket upward.
            flip=np.diag([1,-1,-1,1]);flip[2,3]=14
            loc.apply_transform(flip)
        if i in [24,25]:
            flip=np.array([[0,0,1,-(12 if i==24 else 2)],[0,1,0,0],[-1,0,0,0],[0,0,0,1]],dtype=float)
            loc.apply_transform(flip)
        loc.apply_transform(matrix(i))
        left,right=solid(loc),solids[i]
        delta=abs((left-right).volume())+abs((right-left).volume())
        # ASCII OpenSCAD STL coordinates have decimal serialization rounding.
        tolerance=max(0.002,abs(left.volume())*2e-5)
        bounds_error=float(np.max(np.abs(loc.bounds-placed[i].bounds)))
        passed=delta<tolerance and bounds_error<0.0002
        equivalence.append({'component':NAMES[i],'local_export':LOCAL_FOR_INDEX[i],'symmetric_difference_mm3':delta,'tolerance_mm3':tolerance,'max_bounds_error_mm':bounds_error,'pass':bool(passed)})
        if not passed:failures.append(f'Local/placed source mismatch: {NAMES[i]}')
    # Four normalized spacers must equal their corresponding assembly placements.
    spacerpack=load_mesh(PROJECT/'exports'/'standoffs.stl').split(only_watertight=False)
    if len(spacerpack)!=4:failures.append('Spacer pack does not contain exactly four pieces')
    else:
        for j,c in enumerate(spacerpack):
            c.apply_translation([-c.bounds.mean(axis=0)[0],-c.bounds.mean(axis=0)[1],0])
            expected=c.copy();expected.apply_transform(matrix(19+j))
            delta=abs((solid(expected)-solids[19+j]).volume())+abs((solids[19+j]-solid(expected)).volume())
            if delta>0.02:failures.append('Spacer geometry differs between pack and assembly')
    intersections=[];pairs=0;excluded_aabb=0
    for i,j in itertools.combinations(range(len(NAMES)),2):
        pairs+=1
        low=np.maximum(placed[i].bounds[0],placed[j].bounds[0]);high=np.minimum(placed[i].bounds[1],placed[j].bounds[1])
        if np.any(high<=low+1e-8):excluded_aabb+=1;continue
        overlap=solids[i]^solids[j]
        volume=abs(overlap.volume());status=str(overlap.status())
        item={'a':NAMES[i],'b':NAMES[j],'volume_mm3':volume,'status':status,'pass':volume<0.001 and status=='Error.NoError'}
        intersections.append(item)
        if not item['pass']:failures.append(f'Interference {NAMES[i]} / {NAMES[j]}: {volume:.6f} mm3 ({status})')
    master=inspect(PROJECT/'cute_rover_complete.stl');master['path']='cute_rover_complete.stl'
    service_checks=[]
    # Motor installation/removal: remove upper deck with its two carriers,
    # unplug wiring/remove ties, then remove that wheel+hub before lifting.
    # Only declared envelopes can be checked; real harnesses remain unknown.
    for i in list(range(5,9))+[17]:
        removed={18,23,24,27,i}
        if i<9:removed.update({i+4,i+8})
        max_overlap=0.;tested=0
        for dz in [0.25,1,2,5,10,20,40]:
            moving=placed[i].copy();moving.apply_translation([0,0,dz]);ms=solid(moving)
            for j in set(range(len(NAMES)))-removed:
                if np.any(np.minimum(moving.bounds[1],placed[j].bounds[1])<=np.maximum(moving.bounds[0],placed[j].bounds[0])+1e-8):continue
                tested+=1;overlap=abs((ms^solids[j]).volume());max_overlap=max(max_overlap,overlap)
        passed=max_overlap<0.001
        service_checks.append({'part':NAMES[i],'path':'vertical lift after removing deck/carriers and matching wheel+hub for motor; release ties/fasteners first','sampled_lift_mm':[0.25,1,2,5,10,20,40],'tested_overlaps':tested,'maximum_overlap_mm3':max_overlap,'pass':passed})
        if not passed:failures.append(f'Generic service path obstructed: {NAMES[i]}')
    rotation_checks=[]
    for wi in range(9,13):
        max_overlap=0.;tested=0
        centre=matrix(wi)[:3,3]
        for angle in range(0,360,30):
            axis=trimesh.transformations.rotation_matrix(np.deg2rad(angle),[0,1,0],centre)
            moving=placed[wi].copy();moving.apply_transform(axis);ms=solid(moving)
            for j in set(range(len(NAMES)))-{wi,wi+4}:
                if np.any(np.minimum(moving.bounds[1],placed[j].bounds[1])<=np.maximum(moving.bounds[0],placed[j].bounds[0])+1e-8):continue
                tested+=1;overlap=abs((ms^solids[j]).volume());max_overlap=max(max_overlap,overlap)
        passed=max_overlap<0.001
        rotation_checks.append({'wheel':NAMES[wi],'angles_deg':list(range(0,360,30)),'tested_overlaps':tested,'maximum_overlap_mm3':max_overlap,'pass':passed})
        if not passed:failures.append(f'Wheel rotation interference: {NAMES[wi]}')
    base=placed[0]; wheel_bounds=np.vstack([placed[i].bounds for i in range(9,13)])
    envelope=np.vstack([x.bounds for x in placed]);minimum=envelope.min(0);maximum=envelope.max(0)
    result={'method':'OpenSCAD F6 source exports; exact-coordinate topology without repair; manifold3d solid Boolean differences/intersections of all 28 independently exported assembly components. Mating surface contact is intentional. Small numeric volume threshold 0.001 mm3. Placement expectations are an independent record of the audited DEFAULT configuration; updating parameters requires updating these expectations.',
        'scope_limitations':['No purchased hardware dimensions or physical prints are available. Motors are only conservative generic envelopes, not selected component meshes.','No screw/nut/PCB/battery/cable physical envelopes are certified; tolerance, loads, torque and retention need measured fit tests.','Closed topology and Boolean import do not independently prove absence of every triangle self-intersection; OpenSCAD full solid evaluation and independent Boolean operations provide further evidence.','Slicer/G-code and real printer support/bridging/warping results are not certified.'],
        'versions':{n:importlib.metadata.version(n) for n in ['trimesh','manifold3d','numpy']},
        'master_source_sha256':hashlib.sha256((PROJECT/'cute_rover_complete.scad').read_bytes()).hexdigest(),
        'printable_parts':parts,'placed_components':component_reports,'local_placed_equivalence':equivalence,
        'assembly_pair_count':pairs,'pairs_excluded_by_nonoverlapping_aabbs':excluded_aabb,'boolean_intersections':intersections,
        'service_paths':service_checks,'sampled_wheel_rotations':rotation_checks,
        'nominal_dimensions_mm':{'chassis':[150,105,4],'wheel':[45,14],'wheelbase':104,'track':123,'nominal_ground_clearance':5,'shaft_height_above_base':17.5,'gearbox_face_to_wheel':2,'generic_shaft_engagement':6,'deck':[120,76,3],'deck_bottom_z':38,'spacer_height':34,'battery_clear_cavity':[62,32],'battery_floor':2.4,'battery_max_pack_height_with_3mm_top_margin':28.6},
        'measured_assembly_bounds_mm':[minimum.tolist(),maximum.tolist()],'measured_assembly_extents_mm':(maximum-minimum).tolist(),
        'static_ground_clearance_mm':float(base.bounds[0][2]-wheel_bounds[:,2].min()),
        'visual_assembly_mesh':master,'failures':failures,'pass':not failures}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    for p in parts:print(f'{Path(p["path"]).name}: pass={p["pass"]} solids={p["connected_closed_positive_solids"]} extents={p["extents_mm"]}')
    print(f'Assembly: {pairs} pairs; {len(intersections)} Boolean tests; {len(failures)} failures')
    for f in failures:print('FAIL:',f)
    print('Wrote',args.output)
    return int(bool(failures))
if __name__=='__main__':sys.exit(main())

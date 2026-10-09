"""Reproducible existing-STL checks; numpy only. Does not render SCAD or repair meshes."""
from pathlib import Path
import hashlib, json, re, struct
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / '01_Cute_N20_4WD/cute_rover_complete.stl'
raw = path.read_bytes()
if len(raw) >= 84 and 84 + struct.unpack_from('<I', raw, 80)[0] * 50 == len(raw):
    data = np.frombuffer(raw, dtype=np.dtype([('normal','<f4',(3,)),('v','<f4',(3,3)),('attr','<u2')]), offset=84)
    tri = data['v'].astype(float)
    fmt = 'binary'
else:
    coords = re.findall(rb'vertex\s+([-+\d.eE]+)\s+([-+\d.eE]+)\s+([-+\d.eE]+)', raw)
    tri = np.array(coords, dtype=float).reshape(-1,3,3)
    fmt = 'ASCII'
vertices, inverse = np.unique(tri.reshape(-1,3), axis=0, return_inverse=True)
faces = inverse.reshape(-1,3)
edges = np.concatenate([faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]]])
sorted_edges = np.sort(edges,axis=1)
unique_edges, edge_inverse, counts = np.unique(sorted_edges,axis=0,return_inverse=True,return_counts=True)
direction = np.where(edges[:,0] < edges[:,1],1,-1)
balances = np.bincount(edge_inverse,weights=direction,minlength=len(unique_edges))
parent = np.arange(len(vertices))
def root(i):
    while parent[i] != i:
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i
for a,b in unique_edges:
    ra,rb = root(int(a)),root(int(b))
    if ra != rb: parent[rb] = ra
labels = np.array([root(i) for i in range(len(vertices))])
components = []
for label in np.unique(labels):
    mask = labels[faces[:,0]] == label
    t = tri[mask]
    points = t.reshape(-1,3)
    components.append({'triangles':int(mask.sum()),'min_mm':points.min(0).tolist(),'max_mm':points.max(0).tolist(),
                       'signed_volume_mm3':float(np.einsum('ij,ij->i',t[:,0],np.cross(t[:,1],t[:,2])).sum()/6)})
area = np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2
canonical_faces = np.sort(faces,axis=1)
report = {'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(raw).hexdigest(),'format':fmt,'bytes':len(raw),
          'triangles':len(tri),'vertices':len(vertices),'edges':len(unique_edges),
          'min_mm':vertices.min(0).tolist(),'max_mm':vertices.max(0).tolist(),'extent_mm':np.ptp(vertices,axis=0).tolist(),
          'boundary_edges':int((counts==1).sum()),'nonmanifold_edges':int((counts>2).sum()),
          'inconsistently_oriented_two_face_edges':int(((counts==2)&(balances!=0)).sum()),
          'zero_area_triangles':int((area<1e-10).sum()),
          'duplicate_faces':int(len(faces)-len(np.unique(canonical_faces,axis=0))),
          'nonmanifold_edge_details':[{'vertices_mm':vertices[e].tolist(),'incident_faces':int(c)} for e,c in zip(unique_edges,counts) if c>2],
          'vertex_connected_components':len(components),'surface_area_mm2':float(area.sum()),
          'signed_volume_mm3':float(sum(c['signed_volume_mm3'] for c in components)),
          'components':sorted(components,key=lambda c:c['triangles'],reverse=True),
          'limitations':['Exact-coordinate vertex welding; no near-vertex merging.','No triangle self-intersection check.',
                         'Connectivity is vertex based; it does not prove independent printability.',
                         'No OpenSCAD F6 render or source-to-mesh Boolean comparison performed.']}
(ROOT/'review/stl_metrics.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='components'},indent=2))
print('Component bounds:',json.dumps(report['components']))

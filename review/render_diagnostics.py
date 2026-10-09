"""Source-derived diagnostic diagrams and an existing STL projection; not SCAD renders."""
from pathlib import Path
import os, re
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/rover-review-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
OUT=Path(__file__).resolve().parent
(OUT/'images').mkdir(exist_ok=True)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(1,3,figsize=(15,5),layout='constrained')
ax=axs[0]
ax.add_patch(Rectangle((-75,2),150,4,color='#d5a72e',label='Base: z=2–6'))
for x in [-52,52]: ax.add_patch(Circle((x,26.5),22.5,fill=False,lw=2,color='#138e91'))
ax.axhline(4,color='#c73737',ls='--',label='Wheel ground plane: z=4')
ax.add_patch(Rectangle((-60,38),120,3,color='#d5a72e'))
for x in [-50,50]: ax.add_patch(Rectangle((x-4,4),8,32,color='#6f7581'))
ax.annotate('2 mm deck gap',xy=(-50,37),xytext=(-25,53),arrowprops={'arrowstyle':'->'})
ax.annotate('Base extends 2 mm below ground',xy=(0,2),xytext=(-72,-10),arrowprops={'arrowstyle':'->'})
ax.set(xlim=(-90,90),ylim=(-15,65),title='Compact SCAD: X–Z section',xlabel='X (mm)',ylabel='Z (mm)')
ax.set_aspect('equal');ax.legend(fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.15))
ax=axs[1]
for y in [-125,125]:ax.add_patch(Rectangle((-165,y-14),330,28,color='#7c8490',alpha=.6))
for y in [-55,55]:ax.add_patch(Rectangle((-125,y-12),250,24,color='#e4a62f',alpha=.8))
for x in [-150,150]:
 for y in [-150,150]:ax.add_patch(Rectangle((x-50,y-16),100,32,facecolor='#138e91',alpha=.6))
ax.annotate('Crossmembers run parallel to rails',xy=(0,55),xytext=(-185,0),arrowprops={'arrowstyle':'->'})
ax.annotate('Wheel / rail overlap in projection\n(and actual volume)',xy=(140,136),xytext=(-175,190),arrowprops={'arrowstyle':'->'})
ax.set(xlim=(-220,220),ylim=(-220,220),title='Rugged SCAD: top projection',xlabel='X (mm)',ylabel='Y (mm)');ax.set_aspect('equal')
ax=axs[2]
angles=np.deg2rad(np.arange(0,360,60))
for r,col,label in [(17.9,'#c73737','Current radius 17.9'),(15.5,'#138e91','Reference radius 15.5')]:
 ax.add_patch(Circle((0,0),r,fill=False,color=col,ls='--'))
 ax.scatter(r*np.cos(angles),r*np.sin(angles),s=55,color=col,label=label)
ax.add_patch(Circle((0,0),15,fill=False,lw=2,color='#7c8490',label='Current Ø30 central opening'))
ax.annotate('Corrected screw holes would\nopen into Ø30 clearance',xy=(15.5,0),xytext=(-24,-25),arrowprops={'arrowstyle':'->'})
ax.set(xlim=(-30,30),ylim=(-30,30),title='Rugged motor plate: hole pattern',xlabel='mm',ylabel='mm');ax.set_aspect('equal');ax.legend(loc='upper center',fontsize=8)
fig.suptitle('Analytical CAD findings — current source dimensions, 3 October 2026',fontsize=15)
fig.savefig(OUT/'images/cad_diagnostics.png',dpi=160);plt.close(fig)
raw=(OUT.parent/'01_Cute_N20_4WD/cute_rover_complete.stl').read_bytes()
tri=np.array(re.findall(rb'vertex\s+([-+\d.eE]+)\s+([-+\d.eE]+)\s+([-+\d.eE]+)',raw),dtype=float).reshape(-1,3,3)
fig=plt.figure(figsize=(11,6));ax=fig.add_subplot(111,projection='3d')
ax.add_collection3d(Poly3DCollection(tri,facecolor='#57a5af',edgecolor='none',alpha=.92))
mn=tri.min(axis=(0,1));mx=tri.max(axis=(0,1));ax.set_xlim(mn[0],mx[0]);ax.set_ylim(mn[1],mx[1]);ax.set_zlim(mn[2],mx[2]);ax.set_box_aspect(mx-mn)
ax.set(xlabel='X (assumed mm)',ylabel='Y (assumed mm)',zlabel='Z (assumed mm)',title='Existing compact STL — 227.43 × 172.50 × 48.93 mm\nGeometry differs from current compact SCAD; do not print as a released assembly')
ax.view_init(elev=28,azim=-55);fig.savefig(OUT/'images/existing_stl.png',dpi=150,bbox_inches='tight');plt.close(fig)
print('Saved cad_diagnostics.png and existing_stl.png')

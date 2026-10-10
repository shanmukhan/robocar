#!/usr/bin/env python3
"""Create CAD contact sheet and dimension views from actual generated artifacts."""
from pathlib import Path
import json
import numpy as np
import os
os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/cute-cad-matplotlib")
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from PIL import Image
import trimesh
ROOT=Path(__file__).resolve().parents[2]
report=json.loads((ROOT/'audit/validation_results.json').read_text())
plt.rcParams.update({'font.size':10,'font.family':'DejaVu Sans'})
fig,axes=plt.subplots(4,4,figsize=(16,16),layout='constrained')
for ax in axes.flat:ax.axis('off')
for ax,r in zip(axes.flat,report['printable_parts']):
    path=ROOT/r['path'];ax.imshow(Image.open(path.with_suffix('.png')));ax.axis('off')
    ext=' × '.join(f'{v:.1f}' for v in r['extents_mm'])
    ax.set_title(f'{path.stem}\n{ext} mm; {r["expected_solids"]} solid(s)',fontsize=11)
fig.suptitle('Cute N20 CAD — validated printable meshes in export orientation\nGeneric prototype: hardware fit and printer capability unverified',fontsize=15)
fig.savefig(ROOT/'audit/parts_preview.png',dpi=150);plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(16,8),layout='constrained')
for ax,indices,title in zip(axes,[(0,1),(0,2)],['Top: front is −X; axles along Y','Side: nominal ground at Z=−5 mm']):
    for i in range(len(report['placed_components'])):
        mesh=trimesh.load_mesh(ROOT/'audit/components'/f'component_{i:02d}.stl',process=False)
        col='#328fa8' if i==27 else '#c6a823' if i<5 or 18<=i<=22 or i==26 else '#b4b8bc' if i<9 else '#333333' if i<17 else '#ed9226'
        poly=PolyCollection(mesh.triangles[:,:,indices],facecolors=col,edgecolors='none',alpha=0.9)
        ax.add_collection(poly)
    ax.autoscale_view();ax.set_aspect('equal');ax.grid(alpha=0.2);ax.set_title(title)
    ax.set_xlabel('X (mm)');ax.set_ylabel('Y (mm)' if indices==(0,1) else 'Z (mm)')
    if indices==(0,2):
        ax.axhline(-5,color='#418953',lw=1.4,ls='--',label='Nominal ground')
        ax.annotate('Base underside Z=0\nNominal clearance 5 mm',xy=(10,0),xytext=(10,-26),arrowprops={'arrowstyle':'->'})
        ax.annotate('Deck underside Z=38\nSpacers 34 mm',xy=(30,38),xytext=(90,51),arrowprops={'arrowstyle':'->'})
    else:
        ax.annotate('FRONT −X',xy=(-89,0),xytext=(-114,18),arrowprops={'arrowstyle':'->'})
        ax.text(-110,-105,'Chassis 150 × 105 mm\nWheelbase 104 mm; track 123 mm\nOverall 164 × 137 mm (printed parts + motor envelopes)',fontsize=10)
    ax.set_xlim(-125,135);ax.set_ylim((-110,95) if indices==(0,1) else (-35,90))
fig.suptitle('Current source geometry — millimetres; motors are generic envelopes\nActual static tread clearance 4.949 mm; hardware/cables/battery omitted',fontsize=15)
fig.savefig(ROOT/'audit/assembly_dimensions.png',dpi=170);plt.close(fig)
print('Wrote parts_preview.png and assembly_dimensions.png')

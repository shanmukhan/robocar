# Complete Rover CAD Pack

Two independent parametric CAD designs are included.

1. `01_Cute_N20_4WD` — 150 mm-class compact 4WD rover using N20 motors.
2. `02_Rugged_37D_Future_Proof` — 360 x 290 mm modular 4WD rover using 37D-class encoder motors.

The SCAD files are intended to be edited in OpenSCAD and exported to STL/3MF.

## Important engineering note
No exact motors have been purchased yet. Therefore both motor interfaces are parameterized/generic rather than pretending that every N20 or 37D motor has identical dimensions.

For the rugged rover, the geometry follows the published 37D family envelope, but the exact purchased motor should be checked before final printing.

## Workflow
1. Open the master SCAD.
2. Inspect `assembly()`.
3. Select an individual module.
4. F6 render.
5. Export STL.
6. Print one fit-check part.
7. Verify the purchased motor/wheel/battery.
8. Freeze dimensions.
9. Print the complete set.

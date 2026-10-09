# Cute N20 4WD rover — audited parametric prototype

The geometry has been corrected and individual meshes validated. **Production hardware fit remains unverified:** no exact N20 motor, battery, board set or printer profile is selected.

Start with the [CAD audit](audit/CAD_AUDIT.md), [print guide](audit/PRINT_GUIDE.md), and [image audit](audit/IMAGE_AUDIT.md). The [current assembly preview](cute_rover_assembled_preview.png) shows the actual CAD with generic motor envelopes; the root infographics are concept artwork with different dimensions/features.

## Current design

- 150 × 105 × 4 mm chassis, four N20-class geared motors.
- 45 mm nominal × 14 mm wheels; 104 mm wheelbase and 123 mm track.
- Nominal chassis ground clearance 5 mm; displayed treaded-mesh clearance 4.949 mm, excluding hardware protrusions.
- 120 × 76 × 3 mm electronics deck at Z=38, supported by four 34 mm spacers.
- Floor-backed lower battery tray, generic controller carrier, upright camera carrier, three forward sensor apertures and a mounted bumper.
- Front is **−X**; wheel/shaft axes are along Y.

## Files

`cute_rover_complete.scad` is authoritative. `parts/*.scad` select individual geometry with matching `$fn=96`; wheel/camera/ToF wrappers apply practical print rotations.

[exports/](exports/) contains **12 STL/CSG/PNG sets**: 11 vehicle part types and one optional fit coupon. Every mesh is closed and manifold; `standoffs.stl` intentionally includes four separate spacers. A [prototype print pack](cute_rover_prototype_print_pack.zip) includes the individual exports, sources, guide and previews. Quantities and dimensions are in [printable_parts.csv](audit/printable_parts.csv).

**Do not print `cute_rover_complete.stl` or `parts/assembly.scad`.** The complete assembly includes generic motor envelopes and contacting assembled pieces. Use only individual print exports after checking the guide and actual hardware.

`audit/baseline/` preserves all original Cute files. `audit/` contains findings, reproducible scripts, hashes, topology/interference/self-intersection evidence, hardware probes and dimension/part views. Other projects and root artwork were left unchanged.

## Hardware fit before final printing

Measure motor can and gearbox lengths separately, widths/heights, shaft axis/diameter/flat/usable length, front pilot and terminals. Update `N20_BODY_*`, `N20_GEARBOX_*`, `N20_SHAFT_*` and mating clearances accordingly; the original 25 mm can + 6 mm gearbox and 8 mm shaft are generic placeholders.

Select and measure the battery, ESP32-S3/camera, three ToF breakouts, both drivers, regulator, switch and connectors. Their complete mounting, wiring and insertion paths are not verified by this generic CAD. Print a coupon and one motor/wheel/hub fit set before the full vehicle.

Wheel bolts need **14 mm effective under-head length** (M3×14, or M3×16 with 2 mm head-side spacers); unspaced M3×16 tips collide with the saddles. The radial lock uses a **headless M3 grub screw**. Confirm actual nut/thread fit, retention and wheel runout.

Follow the [reproduction commands](audit/CAD_AUDIT.md#reproduce-the-audit) to regenerate and recheck changes. Validation expectations describe the audited default configuration; changed parameters require a new mechanical review.

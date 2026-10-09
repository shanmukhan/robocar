# Cute N20 4WD CAD and print-readiness audit

**Audit date:** 2026-10-09. **Geometry verdict:** corrected prototype meshes pass the recorded checks. **Production verdict:** UNVERIFIED; exact hardware and a physical printer fit test are still required. The supplied `goal.md` ends at “9. Identify parts”; this audit covers all available instructions, including the image verification in its objective.

## Deliverables and authority

- [Master SCAD](../cute_rover_complete.scad) is the authoritative parametric geometry. `parts/*.scad` select its modules and explicitly set the same `$fn=96`.
- [Prototype print pack](../cute_rover_prototype_print_pack.zip) bundles the selected sources, exports and guide.
- [Individual print exports](../exports/) contain 12 STL/CSG/PNG sets. There are 11 vehicle part types plus one fit coupon. `standoffs.stl` intentionally contains four separate spacers; the other files contain one solid each.
- [Current assembly render](../cute_rover_assembled_preview.png), [dimension views](assembly_dimensions.png), and [part previews](parts_preview.png) are generated from current source/meshes. Silver motor shapes are generic clearance envelopes.
- `cute_rover_complete.stl`, `cute_rover_complete.csg`, and `parts/assembly.scad` describe the assembled vehicle, including motor envelopes. **Do not print the complete assembly STL.** Print individual parts.
- [Baseline](baseline/) preserves every original Cute project file, including the old STL, SCAD, CSG, PNG, wrappers and documents. [Baseline inventory](baseline_inventory.json) records original file hashes. [Initial findings](INITIAL_FINDINGS.md) and [baseline mesh metrics](baseline_mesh_metrics.json) retain the before-correction evidence.
- No STEP/STP/3MF files, real component models, slicer projects, G-code, or physical test results were supplied. No selected motor, battery or PCB drawing establishes actual purchased fit.
- The Rugged project, root documents, root `images/`, and historical `review/` are outside the edit scope. Their original files were left unchanged; four additional root images appeared during the audit and were included in the image review. All current root images were inspected; see [image audit](IMAGE_AUDIT.md).

## Defects corrected

| Original defect | Resulting behavior |
|---|---|
| Base at Z=2..6; underside below wheel ground | Base at Z=0..4; nominal ground clearance 5 mm |
| Blind base holes and ineffective cable slots | Cutters extend beyond both faces; mounting and strap/cable openings are through |
| Motor cylinder cavity ignored body height | Separate rectangular can/gearbox envelopes use width, height and length parameters |
| Mounts embedded in base; holes had no mates | Local bottom datum, matching base holes, exposed screw seats and driver paths |
| Incorrect side insertion and missing retention | Mirrored open-top saddles, two transverse tie channels, low gearbox stop; rails below can top allow ties to press the motor |
| Wheels intersected chassis/gearbox | Wheel inboard face derived from motor face plus clearance; gearbox and shaft remain coaxial |
| Adapter split into two halves; wheel had no interface | One connected adapter, matched flange/sleeve pocket and three axial bolts |
| Loose round bore could not retain wheel | Captured-nut radial **headless M3 grub screw** interface and matching wheel driver window; actual shaft fit/torque remains unverified |
| Hub axial/radial hardware overlapped | Radial screw rotated to the free 30° sector between axial bolts |
| Wheel access opening left a thin lip | Window reduced to Ø4.4 mm, leaving a 2.3 mm axial lip |
| Battery tray lacked floor; screws lay in cavity | 2.4 mm floor, external tabs with shared base holes, two aligned strap routes |
| Standoffs collided with brackets and missed deck | Four shared positions (±50,±14), 34 mm spacers touching base/deck |
| Deck opening retained a roof | Full through cable aperture moved clear of carrier mounting holes |
| ESP carrier lacked mating deck holes | Shared four-hole carrier/deck pattern; PCB-specific attachment still unverified |
| Camera floated and faced sideways | Supported upright front carrier, shared fasteners and accessible screw heads |
| Camera gussets obstructed tools | Gussets moved clear of heads/tool envelopes |
| ToF bar intersected mounts and faced sideways | Forward-facing carrier at −X, bolt tabs clear of motor mounts |
| Bumper detached and collided with wheels | Front bumper with central mounting foot and shared holes |
| Bumper blocked ToF apertures | Optical aperture lower edges sit 2 mm above bumper top; actual sensor field of view remains unverified |
| Front mounting tabs/edge webs were too thin | Inboard fastening patterns; supported tabs; ToF bar widened to 90 mm for ≥2.5 mm outer slot-edge ligament |
| Part exports retained assembled offsets/poor orientations | All export minima Z=0; wheel pocket faces up, camera/ToF rear faces lie on bed |
| Wrappers omitted master tessellation | Explicit 96 segments; small holes no longer use five-sided default cylinders |
| Existing complete STL was stale/non-manifold | Original preserved; current assembly regenerated; separate print meshes supplied |
| Documents and illustrations drifted from CAD | Cute README/planning dimensions updated; root artwork marked conceptual in image audit |

## Current dimensions

All values are millimetres. STL does not encode units; import these files as **mm**.

| Item | Audited default |
|---|---:|
| Chassis plate | 150 × 105 × 4 |
| Wheels | Ø45 nominal × 14; treaded mesh bounding diameter 44.898 |
| Wheelbase / track between wheel midplanes | 104 / 123 |
| Overall assembly, without real hardware/wiring | 164 × 137 × 71.949 |
| Base underside / shaft height | Z=0 / Z=17.5 |
| Nominal wheel ground / nominal base clearance | Z=−5 / 5 |
| Static mesh ground clearance in displayed orientation | 4.949 |
| Upper deck / underside height | 120 × 76 × 3 / Z=38 |
| Standoff diameter / height | 8 / 34 |
| Battery cavity / floor | 62 × 32 / 2.4 |
| Battery space to deck, reserving 3 mm above pack | 28.6 high; connector/strap exit must also fit |
| Original generic motor can | 25 long × 12 wide × 10 high, excluding gearbox |
| Original generic gearbox | 6 long × 12 wide × 12 high |
| Generic shaft / projection / engagement | Ø3 / 8 / 6 |
| Gearbox face to wheel inboard face | 2 |
| Wheel to saddle nose axial gap | 0.5; print growth/runout needs a real fit and spin test |
| M3 clearance / captured nut allowances | Ø3.4 / 5.7 across flats × 2.7 high |
| Hub/wheel radial fit allowance | 0.4 diametral |
| Motor lateral fit allowance | 0.3 each side; axial overrun only 0.02, not a validated FDM allowance |

The 25+6 mm motor lengths and 8 mm shaft are inherited illustrative dimensions, **not a chosen N20 specification**. For comparison only, [Pololu's micro gearmotor family](https://www.pololu.com/category/60/micro-metal-gearmotors) publishes a 10×12 mm gearbox cross-section and 9 mm D shaft, with version-dependent body/gearbox/endcap details in its [dimension drawing](https://www.pololu.com/file/0J1487/pololu-micro-metal-gearmotors.pdf). Those dimensions were not substituted for an unselected vendor's motor.

## Validation evidence

[Export manifest](export_manifest.json) records OpenSCAD version, source/artifact hashes, commands, render summaries and logs. All 40 jobs succeeded with no reported warnings/errors: 12 individual parts, 27 independent placed components, and the visual assembly. Current exports use OpenSCAD 2026.10.08 with its Manifold solid backend.

[Validation results](validation_results.json) record:

- All 12 print meshes have finite coordinates, positive volume, consistent winding, two incident faces at every exactly welded edge, no boundary/non-manifold edges, no duplicate or degenerate triangles, and their expected number of connected solids.
- All exported parts start at Z=0. Bounds are checked against the matching placed source geometry after reversing print rotations; independent symmetric Boolean differences pass the recorded numerical tolerance.
- All **351 component pairs** are checked. Nonoverlapping bounding boxes exclude 322 pairs; 29 require solid Boolean intersections. No positive-volume interference above 0.001 mm³ is found. Mating surface contact and shaft/bore clearance are intentional.
- Four wheel meshes rotated in 30° increments through a full turn remain clear of the modeled fixed components. This sampling is backed by axial separation and wheel-radius envelopes; it does not measure real tyre/shaft runout.
- Sampled vertical motor extraction and battery-tray extraction pass after removing the upper deck/carriers, releasing fasteners/ties, and removing the relevant wheel/hub for a motor. Real terminal leads, harnesses and selected component insertion paths remain unverified.

[Triangle self-intersection checks](printable_self_intersections.json) independently examine all 12 printable meshes without repairing them: **1,068,572 candidate pairs, zero transverse crossings or coplanar area overlaps detected**. Intersecting/separated controls pass. This is a floating-point diagnostic with a 1e−8 mm positional tolerance and documented near-parallel/tiny-contact limitations; it is not an exact-predicate proof.

[Mechanical review](MECHANICAL_REVIEW.md) and [hardware probe results](hardware_checks/nominal_hardware_results.json) check provisional M3 nut/head and driver envelopes independently. These use declared nominal hardware, not purchased fastener measurements. The old radial angle intentionally reproduces a hardware collision; the corrected 30° layout clears it. See the report for exact probe scope and assumptions.

The preserved old assembly STL had a non-manifold edge with four incident faces and extents 227.4263×172.5×48.9263, unlike the original source assembly's 150×138×48. Neither that old file nor a rendered picture was used as proof of printing readiness.

## Printing and assembly

[PRINT_GUIDE.md](PRINT_GUIDE.md) and [printable_parts.csv](printable_parts.csv) cover every printable file, quantities, orientation, local minimum features, bed contact, bridging, supports, warping and remaining fit checks. These are prototype process assessments; no slicer or printer was supplied, and no G-code or physical printing claim is made. The saddle has a supported 1 mm tie-channel bottom skin and ~0.98 mm rear lip, and the hub a ~1.65 mm nut-pocket skin; these intentional prototype sections need physical strength assessment. The installed battery floor covers central base cable openings, so they are not an assembled through-wire route.

1. Measure/select the actual motor, pack, boards, sensor/camera modules and hardware. Update the exposed dimensions and redesign the generic PCB/tie interfaces where necessary.
2. Import the coupon as mm and print it using the intended profile. Measure holes and revise allowances. Print **one** motor saddle, wheel and hub only after motor dimensions are known.
3. Install motor saddles on the base, with nuts below the plate; insert motors vertically and feed two cable ties through each saddle's transverse channels. Ensure ties load the can rather than the rails and clear terminals.
4. Load each hub's axial nuts from its inboard face and the radial nut through its open top slot. Align the wheel's 30° radial window and three bolt holes; fasten wheel to hub, then install on the shaft. Use axial bolts with 14 mm effective under-head length (M3×14 or M3×16 plus 2 mm head-side spacers); unspaced M3×16 collides with the saddles. Use a headless radial M3 screw with the correct tip and a measured usable shaft engagement. Check spin and axial retention.
5. Thread battery straps through the matching tray/base routes before fastening the tray. Verify pack/connector clearance and removal without loading cells with screws.
6. Install four spacers and the deck. Front camera holes share the front spacer fasteners; two extra camera fasteners and the ESP carrier holes match the deck. Install real electronics using measured fixtures/spacers and accessible connectors.
7. Fit forward sensor carrier and bumper. Verify the actual optical field of view, not only the modeled apertures.
8. For motor service remove deck/carriers, disconnect leads, release ties and remove that wheel/hub before lifting the motor. Battery service needs upper-deck removal; no battery door is modeled.

## Unverified release conditions

| Interface or behavior | Required evidence |
|---|---|
| Four N20 motors | Exact manufacturer/SKU/drawing; can and gearbox sizes separately; shaft axis offset, diameter/flat/usable length; front pilot/boss, terminals and any encoder envelope; voltage/ratio and load limits |
| Motor restraint and wheel coupling | Actual axial fit, tie dimensions/preload, grub-screw tip/thread engagement, shaft contact, measured radial/axial runout and retention/torque test; shorten/add hardware-specific clamp if required |
| Battery | Pack chemistry/dimensions/mass including connector/bend radius; strap width/route, removal and protected fastener clearance |
| ESP32-S3/camera | Exact PCB outline, lens/PCB position, hole/strap pattern, underside solder/header clearance, USB/ribbon/antenna access and necessary spacers |
| 2×DRV8833, regulator, fuse, switch, connectors | Exact module dimensions/mounting and wiring bends. They have **no verified fixtures/envelopes** in this CAD. Spare deck area is not proof that the complete electronics set fits |
| 3×ToF breakouts | Actual PCB/optic orientation and footprint, tie or bolt interface, field of view and any desired side angles. Generic straight-ahead apertures are not sensor-specific PCB mounts |
| Hardware | Chosen M3 nut/head dimensions, washers, lengths and thread engagement; long spacer/camera stacks and wheel bolts must be measured; below-base protrusions consume ground clearance |
| Printing | Printer/nozzle/material/profile, calibrated XY/holes, supported bridges, adhesion/warping, fastener pocket fits and a real fit coupon |
| Structure and performance | Payload, printed-material strength/creep, bumper impact, wheel traction, motor shaft radial loads and actual loaded ground clearance |

No production-fit claim is made for any of these unresolved interfaces. Print meshes are geometrically validated prototype assets; physical production release remains conditional on these measurements and tests.

## Reproduce the audit

[Toolchain notes](tooling/TOOLCHAIN.md) record temporary provisioning and original checks. Temporary tools may be removed by macOS. Install the pinned [Python dependencies](tooling/requirements.txt) into your own environment and point to a compatible OpenSCAD CLI:

```sh
python audit/tooling/export_cad.py --openscad /path/to/OpenSCAD --part-previews
python audit/tooling/validate_cad.py
python audit/tooling/check_self_intersections.py exports/*.stl --output audit/printable_self_intersections.json
python audit/tooling/check_hardware_access.py --openscad /path/to/OpenSCAD
python audit/tooling/render_audit_views.py
```

Run from `01_Cute_N20_4WD`. The validator's independently recorded placement expectations describe the **audited default configuration**. Parameter changes require updating those expectations and redoing the mechanical review; successful rendering alone cannot release a changed design. STL/manifold checks do not replace slicer or physical acceptance.

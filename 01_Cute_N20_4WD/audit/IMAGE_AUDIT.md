# Cute Car image audit

Audited 9 October 2026. **All six raster images currently under the repository-root `images/` directory were opened and visually inspected.** Two dual-rover infographics were present at the initial audit; four additional Cute/reference sheets were discovered at the final scope check and assessed against the final corrected CAD. The historical Cute preview, corrected preview, part previews and dimension drawing were also inspected. The historical diagnostic image in `review/images/` was inspected for context. Root images and the unrelated Rugged project were left untouched.

**Verdict:** None of the six root images is an accurate rendering or verified dimensioned drawing of the supplied Cute CAD. All are concept references. Their broad compact four-wheel-drive theme agrees with the project intent, but pictured components, body geometry and numeric specifications cannot certify the CAD or a physical build.

## Scope and provenance

| Inspected file | Classification | SHA-256 of inspected image |
|---|---|---|
| [`Dual Rover Design Breakdown Infographic.png`](../../images/Dual%20Rover%20Design%20Breakdown%20Infographic.png) | Concept illustration of two vehicles; not an exported CAD assembly or exploded drawing | `9cccea6e99bc719c332aa5d83e4a2ac90b3c4a4c86363609c632e56fc38a0fed` |
| [`Dual Rover Technical Comparison Infographic.png`](../../images/Dual%20Rover%20Technical%20Comparison%20Infographic.png) | Concept comparison; approximate captions conflict with the pre-correction source | `d6a4cb76b580189e4d4b97e2798cb077f48ea9530bd02376946071135392ac2f` |
| [`Cute 4WD Robot Car Orthographic Sheet.png`](../../images/Cute%204WD%20Robot%20Car%20Orthographic%20Sheet.png) | Concept/reference vehicle with two decorative sensor eyes, upper battery and bought wheels | `731dde54691201240b47e7b580fea143e0dc1809283cdb0e1b061410510ff013` |
| [`DIY Robot Rover Orthographic View Sheet.png`](../../images/DIY%20Robot%20Rover%20Orthographic%20View%20Sheet.png) | Concept/reference vehicle; overall dimension arrows confuse chassis and wheel envelope | `0a759e4375c7814887820e581e1c780e42d24841e4a29f203b84125fefb32724` |
| [`Six-View Colorful Robot Rover Assembly Sheet.png`](../../images/Six-View%20Colorful%20Robot%20Rover%20Assembly%20Sheet.png) | Concept/reference vehicle with illuminated eyes and a different enclosure/drivetrain | `e6e63b084542bcffac9babe4845a4ecf3025eb0d060b07a17489a2883d02e55d` |
| [`Yellow 4WD Robot Rover Assembly Guide.png`](../../images/Yellow%204WD%20Robot%20Rover%20Assembly%20Guide.png) | Concept assembly guide; illustrated interfaces and component specifications are unverified | `05ce1ff4aa86c400e31df01f4237ca2bb1faeb296fa74909d13306999390fd0c` |
| [`baseline/cute_rover_assembled_preview.png`](baseline/cute_rover_assembled_preview.png) | Historical CAD-style perspective preview; source revision and render method unverified | `a21efa9d47fd8ad42afad1cd8641a48247250b0a59bd64e07bd933fdf6b431c3` |
| [`cad_diagnostics.png`](../../review/images/cad_diagnostics.png) | Historical analytical diagram, including both projects; not an assembly rendering | Not an authoritative export |

The Cute preview's filesystem timestamp was 18 seconds after the original master SCAD timestamp. That timing does not establish the source hash, renderer, F5/F6 mode, camera settings or Boolean validity. The preview hash above identifies the version actually inspected; if the preview is regenerated at the same path, this audit's historical observations refer to that hash.

## Dimensions before correction

**Every source dimension in this section is from `cute_rover_complete.scad` BEFORE the current correction.** These values document why the existing artwork failed comparison. They are not specifications for the corrected revision. Use the corrected CAD, measured exports and new generated views for current dimensions.

| Item | Car 1 captions in both root infographics | Original source evidence and comparison |
|---|---|---|
| Length | 150 mm | `CHASSIS_L = 150`; broad chassis-length agreement |
| Width | 110 mm | `CHASSIS_W = 105`; the artwork does not distinguish chassis width from wheel/shaft envelope |
| Height | 70 mm | Source nominal assembly spans Z = 2 to 50, approximately 48 mm; no 70 mm tall enclosed body or upright installed camera is present |
| Wheel diameter | 42 mm | `WHEEL_D = 45`; source wheel width is 14 mm, also differing from the planning document's 12 mm |
| Ground clearance | 12 mm | Base Z = 2 to 6 and nominal wheel ground Z = 4 give approximately **−2 mm** underside clearance; this is a source defect, not usable vehicle clearance |
| Mass | Approximately 300–400 g | No verified hardware mass, material density/infill calculation, sliced result or weighing supports this estimate |
| Wheelbase | Not dimensioned | Wheel centres at X = ±52 imply 104 mm |
| Wheel-centre track | Not dimensioned | `SIDE_Y = 58.5` implies 117 mm |
| Overall width | Not distinguished | Nominal tyre envelope 131 mm; integral hub envelope 133 mm; visual motor shaft tips extend to Y = ±69, giving approximately 138 mm |

These are analytical nominal bounds, not fresh mesh measurements. The original cylinders are polygonal and tread cuts remove some extremal wheel material; exact rendered wheel bounds and resulting ground-plane position require mesh measurement. The negative-clearance conclusion remains: the chassis underside lies below the nominal wheel contact plane. The original top camera fixture reaches Z = 50; height is measured from the base minimum Z = 2, not from an assumed zero datum.

## Design Breakdown infographic

The top section correctly conveys a small yellow four-wheel-drive rover and names several intended component families: N20 motors, ESP32-S3, two DRV8833 modules, ToF sensing, a 2S battery and a logic-power module. These are planning-level agreements. The image does not establish the exact purchased variants, mounting patterns, dimensions, wiring or fit.

The following discrepancies prevent using it as the Cute CAD assembly reference:

| Pictured or labelled detail | Comparison with original Cute CAD |
|---|---|
| Sculpted yellow shell with side panels and fenders | Source `top_cover()` aliases a flat 120 × 76 × 3 mm electronics deck; the illustrated enclosed body does not exist as corresponding printable CAD |
| Spoked yellow wheels with rounded black tyres | Source wheels are solid grooved disks with a central round bore and raised integral hub; the illustrated wheel/hub construction is different |
| Upright camera on the top-front body | The assembly uses a horizontal slotted `camera_mount()` fixture. A separate `camera_front_mount()` is defined but never called; no exact installed camera envelope is modelled |
| Two prominent forward circular “eyes” and lights | Source ToF bar has three vertical Ø8 mm apertures, not the depicted pair of forward-facing circular features. Matching light parts and interfaces are absent |
| Antenna, rear USB-like opening, power switch and finished enclosure | No matching installed antenna, port or switch geometry is defined by the source |
| Detailed electronics layout and wiring | Source contains generic trays, without component-specific PCB, connector, regulator and wiring envelopes; the picture is not a verified packaging check |
| Battery and electronics stack in exploded view | Pictured pack and stacked boards are not linked to exact CAD interfaces or verified battery dimensions. The original battery tray itself has no intact floor |
| `4 × N20 Geared Motors (12V, ~60 RPM)` | No exact motor SKU, rated voltage or ratio was frozen in the project. Earlier review planning discusses a 6 V / 100 RPM option. The artwork's motor specification is **unverified** |
| “Main Parts” exploded illustration | Shapes and placements are conceptual; they are not a traceable set of exports from the supplied modules |

Wheel shafts in the original source run along Y, making ±X the rolling direction. Original bumper, camera fixture and ToF bar are placed on the −Y lateral side. The illustrated conventional forward vehicle face therefore cannot verify the source's front direction or sensor aim.

**Per-file verdict:** Retain as a concept and electronics-intent reference only. Do not use its dimensions, motor voltage/RPM, exploded placements or body shapes for fabrication or fit approval. Its Rugged content is outside this Cute-only implementation scope.

## Technical Comparison infographic

Its six Car 1 views consistently communicate the intended appearance of a compact enclosed yellow rover with four wheels and a camera. They do not depict the actual flat-deck CAD parts. All six views show the sculpted body and wheel system described above, and the front/rear views add features for which no corresponding Cute geometry exists.

Front/rear captions repeat 110 mm width; side/top/bottom captions repeat 150 mm length; the key table repeats 70 mm height, Ø42 mm wheels, 12 mm clearance and estimated mass. A repeated number is not measurement evidence. The source comparisons in the pre-correction dimension table apply to every occurrence. The bottom view illustrates a plausible four-motor architecture but does not establish actual motor bracket, gearbox, wheel-shaft engagement or screw compatibility.

**Per-file verdict:** Retain as a concept comparison only. It is unsuitable as a dimensioned Cute drawing or evidence of mechanical compatibility. Its lower Rugged section does not represent Car 1 and is outside this implementation scope.

## Existing Cute assembly preview

The inspected preview is closer to the source's visual structure than the infographics: a rectangular lower chassis, flat upper deck, four grooved solid wheels, orange fixtures/trays, and no fully installed electronics. It is a perspective illustration without axes, scale or dimensional annotations.

The preview is insufficient to verify these original defects:

- Base underside below the wheel contact plane.
- A 2 mm gap between standoff tops and upper-deck underside.
- Wheel/chassis and gearbox/hub interference.
- Detached bumper and mismatched mounting-hole patterns.
- Floating camera fixture, incomplete shaft locking and unresolved sensor-facing direction.
- Exact motor, battery, PCB and connector fit.

Some apparent mounting-hole locations look like raised nubs, and no central through cable opening is visible in the upper deck. Those are image observations, not a reliable topology diagnosis; source geometry and rendered meshes must determine whether a feature is a real hole or rendering artefact. The original deck cutter leaves a roof over its intended cable opening.

**Per-file verdict:** Historical preview with unverified source provenance. It can illustrate broad layout, but cannot certify current-source agreement, assembly fit or print readiness. Regenerate a traceable assembly preview from the corrected source and include labelled axis/dimension views.

## Historical diagnostics and documentation drift

The Cute panel in `review/images/cad_diagnostics.png` correctly illustrates the original source's base Z = 2–6, nominal wheel ground Z = 4 and 2 mm deck-support gap. It is an analytical historical chart, not a corrected assembly view. Preserve it outside the Cute project and refer to it as historical evidence.

The older review says the repository-root images directory was empty. That statement no longer describes the inspected workspace: both root PNGs listed above are present and were inspected. The Cute planning document also references `compact_rover_top.svg`, which was absent during inspection; it is not available as an additional assembly image.

## Current-revision handoff

This document records the image audit and pre-correction comparisons. The corrected revision should supply generated assembly views, current dimensions and source/export provenance in its own audit outputs. Root concepts should remain clearly identified as concepts wherever they are referenced. A rendering alone does not establish hardware compatibility, manifold printable geometry or physical fit.

## Corrected current-CAD assembly render

The current [`cute_rover_assembled_preview.png`](../cute_rover_assembled_preview.png) was regenerated from the corrected master and visually inspected. The previously inspected image is preserved at [`baseline/cute_rover_assembled_preview.png`](baseline/cute_rover_assembled_preview.png); the historical findings above refer to that baseline image. Root infographics remain unchanged concept references.

[`export_manifest.json`](export_manifest.json) records the final corrected source SHA-256 `ab20425c38f1885bc060f11dfb80747b556f0968cb03b06d3ba99658b2f7b2e0`, a successful OpenSCAD solid-render job using the Manifold backend, orthographic camera settings and no diagnostics. The current preview hash is `b742de3ba6cbba016b22764f6801c4949980e89eb7ab08b26dce7a8a4b5cd9fb` and matches that manifest and the actual file inspected. The numerical dimensions below come from [`validation_results.json`](validation_results.json), rather than estimating distances in the picture.

| Current default configuration | Nominal source dimension | Measured exported geometry |
|---|---:|---:|
| Chassis | 150 × 105 × 4 mm | 150 × 105 × 4 mm |
| Complete visual assembly, including bumper and camera fixture | Not the chassis-only footprint | 164 × 137 × 71.949 mm |
| Wheel diameter / width | 45 / 14 mm | Wheel XY extents 44.898 × 44.898 mm; axial width 14 mm |
| Wheelbase / wheel-centre track | 104 / 123 mm | Placed-part checks agree with the default source positions |
| Chassis underside clearance above wheel contact plane | 5 mm | 4.949 mm at the rendered tread orientation |
| Upper deck | 120 × 76 × 3 mm; underside Z = 38 mm | Placed-part checks agree with the default source positions |
| Standoffs | 34 mm tall | 34 mm, joining base top Z = 4 to deck underside Z = 38 |

The new view shows four grooved wheels, open motor saddles, the supported upper deck, a lower battery tray, the upright camera fixture and three forward-facing ToF apertures behind the bumper. Front is now −X and axles run along Y. Through holes and the deck cable opening are visible. Silver rectangular shapes are **generic motor envelopes**, not selected N20 hardware models. Actual camera, ToF boards, controller, drivers, battery, wiring and fasteners are not installed component meshes in this picture.

The recorded validation passes for the exported default configuration: 12 printable exports and 27 placed assembly components were checked, with 351 component pairs considered and no unintended solid-intersection volume above the stated 0.001 mm³ threshold. That evidence supports source/export agreement and the represented geometric layout. The preview itself does not prove measured hardware fit, shaft torque retention, screw/tool insertion, running clearance under load, PCB/connector packaging, print tolerances, supports or a physical assembly. The full-assembly STL is a visualization export; printable parts are the individual files under `exports/`.

## Final part previews and dimension drawing

The final [`parts_preview.png`](parts_preview.png) contact sheet, [`assembly_dimensions.png`](assembly_dimensions.png), regenerated assembly preview and **all 12 individual PNGs under `exports/`** were opened and visually inspected against the final validation record. The contact sheet's measured dimensions and solid counts agree with that record, including four deliberately separate standoffs in one export. Colours are rendering/shading choices, not a specified multi-material print.

| Individual preview | Visible corrected feature |
|---|---|
| [`base_plate.png`](../exports/base_plate.png) | Flat chassis plate, mounting holes and visibly open cable/strap slots |
| [`battery_tray.png`](../exports/battery_tray.png) | Continuous cavity floor, low rim, external mounting tabs and strap passages |
| [`camera_mount.png`](../exports/camera_mount.png) | Mounting holes, open camera-fixture region, tie slots and two supporting gussets; shown in its printable orientation |
| [`esp32_tray.png`](../exports/esp32_tray.png) | Flat generic carrier with four mounting holes and two restraint slots |
| [`fit_coupon.png`](../exports/fit_coupon.png) | Five separate test bores in a single solid block |
| [`front_bumper.png`](../exports/front_bumper.png) | Continuous bumper wall connected to a mounting foot |
| [`n20_motor_mount.png`](../exports/n20_motor_mount.png) | Open-top rectangular saddle, mounting-hole access and transverse tie channels |
| [`standoffs.png`](../exports/standoffs.png) | Four separate spacers with axial holes; intentional copies rather than accidental fragments |
| [`tof_sensor_bar.png`](../exports/tof_sensor_bar.png) | Three apertures with adjacent restraint slots and two mounting tabs; shown in its printable orientation |
| [`top_cover.png`](../exports/top_cover.png) | Flat electronics deck with mounting holes and an open cable passage |
| [`wheel.png`](../exports/wheel.png) | Grooved rim, recessed hub interface and fastening apertures; no spoked rubber tyre is implied |
| [`wheel_hub_adapter.png`](../exports/wheel_hub_adapter.png) | Continuous flange with central bore, axial fastener holes and a nut/retention pocket; the original diameter-wide splitting slot is absent |

No missing part, detached unintended fragment or obviously capped intended opening was apparent in these views. That is a visual cross-check; the mesh/Boolean validation provides the geometric evidence. The PNGs cannot certify hidden geometry, minimum printable resolution or real printer results.

The dimension drawing correctly labels front as −X, axles along Y, chassis 150 × 105 mm, wheelbase 104 mm, track 123 mm and overall footprint 164 × 137 mm including printed fixtures and generic motor envelopes. Its side view labels the base underside Z = 0, deck underside Z = 38 and 34 mm spacers. The dashed ground line is explicitly **nominal** Z = −5 mm; the header separately gives measured static tread clearance 4.949 mm. Hardware, cables and the actual battery are explicitly omitted. This is a traceable geometric assembly illustration of the parametric prototype, not a finished-product or physically tested hardware drawing.

## Additional root images found at the final scope check

The following four images were not in the initial two-image inventory. They were all subsequently opened, hashed and compared with final source `ab20425c38f1885bc060f11dfb80747b556f0968cb03b06d3ba99658b2f7b2e0` and its validation results. Their origin and source revision are unverified. The audit did not create or modify them. This completes inspection of all six files in the root `images/` directory.

### Cute 4WD Robot Car Orthographic Sheet.png

SHA-256: `731dde54691201240b47e7b580fea143e0dc1809283cdb0e1b061410510ff013`.

Its eight panels show front, rear, two sides, top, bottom and two perspective views. Four wheels, four outward-driven motors and an electronics platform agree with the broad 4WD intent. No numerical scale, motor SKU or traceable CAD source is supplied.

The pictured vehicle has spoked rubber wheels, a contoured yellow face with two circular eyes and a smile slot, a black underside/side enclosure, a top-mounted strapped battery, installed PCB and wiring. Final CAD instead has printed grooved wheels with separate fastening flanges, an open lower battery tray, a flat supported electronics deck, three ToF apertures on a front bar and a separate upright camera fixture. The CAD's upright camera fixture and three-sensor bar are absent from the picture. Its motor/gearbox and bracket detail is not the CAD's generic rectangular envelope in an open saddle retained by ties.

**Verdict:** Concept/reference vehicle, not a final-CAD orthographic sheet. The two pictured eyes do not establish the planned three-ToF arrangement, and the upper battery placement does not verify the lower tray, restraint or centre of gravity. Do not derive motor mounts, wheel offsets, chassis holes or enclosure parts from these views.

### DIY Robot Rover Orthographic View Sheet.png

SHA-256: `0a759e4375c7814887820e581e1c780e42d24841e4a29f203b84125fefb32724`.

Its ten vehicle views broadly resemble the intended camera-plus-three-front-sensors 4WD configuration. The table's approximately 150 × 105 mm chassis and Ø45 mm wheels agree with nominal source values **only when length/width mean chassis dimensions**. Its stated 70–80 mm height overlaps the generic CAD's measured 71.949 mm assembly height, but the illustrated installed camera and battery are different, unmeasured hardware.

The front-view 105 mm arrow extends between outer wheel edges. That is a consequential dimension error for this CAD: actual overall width is 137 mm, while 105 mm is the base plate width. The side-view 150 mm arrow likewise cannot certify the complete assembly: final front fixtures extend total length to 164 mm. Using the picture as an overall envelope could under-size clearances by 32 mm in width and 14 mm in length.

Other differences include a black perforated upper plate, spoked rubber wheels, upper/rear blue battery pack, purchased-style motor brackets, a rear port aperture and a camera mounted on a circular base. None is the corresponding final printed interface. Source camera/ToF fixtures use generic openings and tie slots, not a verified mounting pattern for the depicted boards. The image also does not define a shaft-locking interface or enough dimensions to verify four purchased motors.

**Verdict:** Concept/reference sheet with some matching nominal numbers and misleading overall-envelope arrows. It is unsuitable for manufacturing dimensions, hardware-fit approval or assembly-hole placement. Use `assembly_dimensions.png` and measured exports for the represented CAD envelope.

### Six-View Colorful Robot Rover Assembly Sheet.png

SHA-256: `e6e63b084542bcffac9babe4845a4ecf3025eb0d060b07a17489a2883d02e55d`.

Its six labelled views consistently convey a cute yellow rover with four wheels and a controller board. They supply no numerical dimensions or traceable source/export information.

The vehicle has two illuminated circular eyes, a smile opening, an enclosing yellow face, black rear/underbody panels, spoked rubber tyres and a large black battery on the upper deck. It lacks the final CAD's visible upright camera fixture and three-position front ToF bar. The illustrated lower motor plate, fastener locations, board carrier and body panels differ from the printed source. No matching mounts for lighting or the illustrated case/connector are defined.

**Verdict:** Styling/reference concept, not the final Cute assembly. The two eyes cannot substitute for the planned three-ToF arrangement, and neither the upper battery nor the enclosed lower motor structure verifies source fit, access or load distribution. No mass, clearance or capability claim can be established from these pictures.

### Yellow 4WD Robot Rover Assembly Guide.png

SHA-256: `05ce1ff4aa86c400e31df01f4237ca2bb1faeb296fa74909d13306999390fd0c`.

This image combines vehicle views, an exploded assembly, component images, layer diagrams, drivetrain detail, camera-tilt detail and dimensional captions. Camera, four motors, three sensors, an ESP-family controller, DRV8833 and a 2S battery broadly match planning intent. Its detailed labels and exploded parts must not be treated as validated assembly instructions.

| Image detail | Consequential disagreement or unverified interface |
|---|---|
| 105 mm width arrows span outer tyres; 150 mm length presented for the complete vehicle | Source 105 × 150 mm values describe the chassis. The corrected assembly measures 137 × 164 mm in plan, including wheels/front fixtures |
| 70–80 mm height and Ø45 mm wheel captions | Nominal wheel value agrees and generic assembly height is 71.949 mm, but pictured installed hardware dimensions remain unverified |
| Top/chassis plates labelled acrylic/FRP | Final source provides printed parametric plates, with different outlines, openings and fastener patterns; pictured commercial plate dimensions are absent |
| Blue battery on the upper/rear platform; labelled 2S Li-ion, 7.4 V, 1500–2200 mAh | Source battery tray is low on the base with a generic 62 × 32 mm cavity and restricted available height. No chosen pack drawing proves that the labelled capacity/chemistry fits |
| Wheel/motor exploded detail with a separate two-screw motor face plate | Final CAD uses an open saddle and a separate wheel flange with three axial fasteners plus radial shaft retention. The illustrated plate/shaft/wheel interface has no matching verified source pattern or selected motor drawing |
| Micro-servo or tilt mechanism under the camera | Final camera fixture is a fixed printed bracket with generic restraint slots. No servo bracket, bearing/pivot, servo envelope or moving-cable clearance is modelled |
| N20 motor labelled 6 V, 100–200 RPM | Voltage and speed are unverified until an exact motor variant and driver/current specification are selected; the final geometry uses generic envelopes |
| ESP32-S3 / ESP32-CAM and pictured electronics stack | Exact board dimensions, GPIO allocation and placement are not established by the image. The current CAD's carrier is generic and does not certify the illustrated stack |
| USB-C power module labelled 5 V, 3 A | A label is not a validated electrical schematic, motor-power interface or regulator thermal/current test |

**Verdict:** Conceptual assembly/reference guide, not an executable build drawing for the supplied CAD. Following its faceplate screws, wheel coupling, plate layers or servo stack would substitute different interfaces without verification. Require the selected hardware drawings and current part/fastener instructions before assembly; use source-derived dimensions rather than the misleading overall arrows.

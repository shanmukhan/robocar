# Cute N20 4WD — corrected mechanical review

Reviewed 2026-10-10 (India), including charger addition. Current master source SHA-256:

`5b93f8ecde6941c00b0bfbacb356c0b4777d9e04ad2e35564c2c5153b0b3768a`

The corrected **default generic geometry** has coherent mating positions, a viable assembly sequence, and clear nominal fastener/tool access under the assumptions below. It is a prototype release: exact motor, battery, PCB, tyre material, printer fit and load capacity remain unverified. The previous revision and its defects are recorded separately in [INITIAL_FINDINGS.md](INITIAL_FINDINGS.md).

## Geometry and mating evidence

The base now occupies Z=0..4. Nominal wheel radius 22.5 and shaft Z=17.5 put the ideal tyre ground plane at Z=−5, giving 5 mm nominal chassis underside clearance. Actual tread contact and hardware protrusions must be checked on the assembled rover.

Four motor saddles share their mounting coordinates with the base. The local motor shaft is along Y; side placement mirrors the negative-Y components. Each generic motor spans local Y=−31..0 with the nominal shaft projecting 0..8. The wheel/hub begins 2 mm outside that gearbox face and engages 6 mm of the nominal shaft. Wheel centres are X=±52,Y=±61.5,Z=17.5, giving 104 mm wheelbase and 123 mm centre-to-centre track. Wheels occupy Y=±54.5..±68.5; hardware is excluded from that envelope.

Standoffs at (±50,±14) now mate with both plates. Their 34 mm height joins base top 4 to deck underside 38. Battery tray and carrier interfaces use shared point arrays. The camera's two holes at global(−50,±14) deliberately share the front deck/standoff fasteners; its two additional holes are at (−40,±10).

Front is−X. Bumper wall is at X=−89..−85,Z=4..20. ToF carrier is behind it at X=−82..−78, with its apertures at global Z=26, lower edge 22, giving 2 mm geometric clearance over the bumper. Its 90 mm beam also clears wheel placement. The camera aperture is higher and points forward. Actual sensor optical fields and module attachment are still unverified.

The bumper's central foot spans X=−87..−59,Y=±6,Z=4..7, with base fasteners at (−71,0) and(−63,0). ToF feet are at Y=±12 and span Y=±7..±17; the nearest printed-foot separation from the bumper is 1 mm. Nominal head/tool envelopes have additional clearance and were checked separately.

## Independent nominal hardware probes

[check_hardware_access.py](tooling/check_hardware_access.py) freezes a source copy, runs OpenSCAD Manifold intersections, deletes previous probe STLs before rendering and rejects unexpected diagnostics or failures. It verifies the source did not change during the run. The latest [nominal_hardware_results.json](hardware_checks/nominal_hardware_results.json) reports `passed: true` against the source hash above.

The probes use real-nut assumptions of AF5.5 ×2.4 mm within CAD pockets AF5.7 ×2.7 mm. Heads are conservatively modelled Ø6.6 ×3 mm. Front carrier socket/tool envelopes are Ø8 mm; motor and radial hub Allen-tool envelopes are Ø3 mm. These are explicitly nominal allowances, not measurements of purchased hardware.

| Probe | Positive intersection volume | Interpretation |
|---|---:|---|
| Camera heads and Ø8 tools versus printed carrier | 0 mm³ | Central gussets clear all four fasteners and tool approaches. |
| ToF heads and Ø8 tools versus printed carrier | 0 mm³ | Raised beam and mounting feet allow access. |
| Bumper heads and Ø8 tools versus printed bumper | 0 mm³ | Central foot allows access to both screws. |
| Motor heads and Ø3 Allen tools versus saddle | Approximately 3.8×10⁻¹⁴ mm³ | Numerical zero; heads and Allen keys clear. |
| Hub nuts, flush bolts, grub screw and driver versus wheel/hub | 0 mm³ | Matching 30° radial window provides access to the headless screw. |
| Radial versus axial hub hardware at 30° | 0 mm³ | Captured nuts and bolts are separated. |
| Flush 14 mm effective wheel bolts versus all four saddles | 0 mm³ | Correct bolt length clears the noses. |
| Deliberate control: radial fastener at old 0° | 0.090512 mm³ | Reproduces the former hardware collision; corrected 30° placement avoids it. |
| Deliberate control: unspaced M3×16 wheel bolts | 63.571771 mm³ | Demonstrates substantial saddle-nose collision from protruding bolt tips. |

The pass threshold is 1×10⁻⁸ mm³. Intended planar seats can produce zero-volume intersection sheets; their STLs are **diagnostic artefacts, not printable parts**, and must not be subjected to manufacturing mesh acceptance. These probes assess positive solid interference; the separate [validation_results.json](validation_results.json) assesses manufacturing exports and printed-component assembly geometry.

### Wheel fasteners must be selected explicitly

Use **M3×14 axial wheel bolts**, or **M3×16 with 2 mm of head-side spacers/washers** to obtain 14 mm effective penetration. Heads face outward; the captured nuts are inboard. Confirm full nut thread engagement and flush inboard tips. A generic unspaced M3×16 fastener kit is incompatible with this interface: protruding tips enter the saddle noses across their 0.5 mm gap.

The radial fastener must be a **headless M3 grub/set screw**, provisionally about 10 mm long, loaded through the captured nut. A socket-cap bolt head will not pass through the Ø3.4 radial bore. Actual length, tip form, shaft-flat contact, tightening torque and motor-shaft damage must be verified with the selected hardware. Keep the wheel window and adapter radial slot aligned at 30°.

Motor flange screws require Allen/socket-head access above the flange, with their nuts below the base. The Ø6.6 head relief is not a certification that an arbitrary Ø8 nut driver fits that motor-flange recess. The vehicle must be lifted for underside nut access.

Other screw lengths follow actual stacks and washers: base+motor/bumper flange is 7 mm; base+ToF foot is 8 mm; base+battery tab is 6.4 mm; deck+ESP/camera carrier is 6 mm; base+spacer+deck is 41 mm, or 44 mm where the camera shares the front spacers. Select hardware after measuring it and check protrusions against the 5 mm ground clearance. Bottom-entering long spacer bolts avoid long screw tips projecting below the chassis.

## Motor, tie and maintenance access

The saddle is open above, with separate supporting levels for nominal 10 mm body and 12 mm gearbox heights. Its sidewall top is local Z16.5, versus motor-body top 18.5. Both ties cross the motor can at local Y=−13.5 and−24.75, so the tie bears on the can rather than resting on a taller rail. Channels are 2.6 mm wide ×2 mm high and have accessible transverse ends. Only measured narrow ties that fit those channels are appropriate.

Install or remove motors vertically with the upper deck removed. Install wheel/hub captured nuts and axial bolts on the bench before sliding each complete wheel outward onto its motor shaft; then tighten the accessible radial grub screw. Wheel removal is outward after loosening that screw. Deck removal provides tie cutting/replacement, motor-terminal and battery service access. These routes are geometrically feasible for the supplied generic envelopes; actual lead exits and boards may change them.

Battery straps pass through aligned base/tray slots. Pack removal is conditional on real pack height and connectors; removal of the deck is the defined service route when the pack cannot lift clear of the shallow rim beneath it. No battery dimensions or wire exits have been invented.

## Wall sections and print orientation

The orientations below are encoded by the printable wrappers; assembled components retain their correct placements.

| Part | Practical orientation / supports | Measured default sections and limits |
|---|---|---|
| Base | Flat underside on bed; no geometric support requirement |4 mm plate;2.8 mm ligament between central and strap slots; front bumper base hole has 2.3 mm edge ligament. |
| Motor saddle | Foot flat on bed; short tie-channel roofs bridge 2.6 mm |3 mm flange; nominal 3 mm sidewalls reduce locally to about 2.4 mm next to head reliefs. Channel bottom skin is 1 mm and is supported by the chassis in assembly. Rear axial stop is about 0.98 mm; do not rely on it as the primary retention mechanism. |
| Wheel | Outboard flat face on bed, pocket upward, using `wheel_print()` |5 mm behind flange pocket;3.8 mm behind deeper hub pocket; at least 4.3 mm gross radial rim at tread grooves; Ø4.4 driver window leaves 2.3 mm inboard lip. Horizontal window may need local support or hole cleanup depending on the printer. |
| Hub adapter | Flat flange on bed; captured-nut openings face bed |Flange 9 mm; approximately 2.71 mm minimum outer ligament around axial nut pockets. Radial nut cavity has an approximately 1.65 mm bottom skin. Small hex-to-bore transitions and radial bore require slicer inspection/cleanup; nut-loading slot is open above. |
| Battery tray | Floor flat on bed; no geometric support requirement |2.4 mm floor; shallow 4.6 mm retaining height; rim around strap apertures has 1.8 mm outer ligament. Tabs have material around M3 holes but strength and battery restraints require a pack-specific test. |
| ESP carrier | Flat plate on bed; no geometric support requirement |3 mm plate;2.7 mm edge beside tie slots; board underside spacing and mounting remain generic. |
| Camera carrier | Broad upright face on bed using `camera_mount_print()` |3 mm plate; lens and tie openings print vertically, avoiding the 20 mm upright lens bridge. Gussets are supported by this orientation. Horizontal Ø3.4 mounting holes are short bridges; fit/cleanup remains printer-dependent. |
| ToF carrier | Broad upright face on bed using `tof_sensor_bar_print()` |4 mm plate/feet; minimum outer tie rail 2.5 mm after widening beam; approximately 1.9 mm between optic and adjacent tie slot. Horizontal Ø3.4 mounting holes are short bridges. Printed orientation avoids supporting the raised beam. |
| Bumper | Wall/central foot on bed; no geometric support requirement |4 mm wall;3 mm foot;2.3 mm ligament beyond last fastener. Material and impact strength remain untested. |
| Four standoffs | Four separate tubes upright on bed; brim if needed |Ø8 with Ø3.4 bore gives 2.3 mm radial wall; height 34. Four intentional separate solids are exported together. |
| Fit coupon | Flat on bed; no geometric support requirement |5 mm plate with 3.1–3.4 mm and nominal shaft-clearance holes. It verifies printer holes only; print one saddle/hub for motor and coupling fit. |

PETG is suitable for the documented prototype intent; actual extrusion width, layer height, supports, bridging, shrinkage and tightening behavior must be assessed in the chosen slicer and a representative print. Geometry inspection cannot certify that every printer can bridge the small channels or preserve fit. Printed rigid wheels also do not establish traction equivalent to purchased rubber tyres.

## Remaining conditions before physical use

- Freeze and measure the exact motor drawing: body and gearbox profiles/lengths, eccentricity, shaft diameter/flat/length, leads and allowable mounting pressure. Generic CAD envelope agreement is not selected-SKU compatibility.
- Test **axial motor fit**: cavity end clearances presently use Boolean EPS≈0.02 mm rather than a calibrated axial FDM allowance. Width has 0.3 mm per-side allowance, but printer shrink or a longer can can prevent insertion.
- Test the **0.5 mm wheel-to-saddle-nose gap** for printer growth, runout, axial movement and wheel spinning. Do not infer dynamic clearance solely from zero static solid intersection.
- Establish real shaft engagement and grub-screw contact. Nominal 6 mm engagement places the 4.5 mm set-screw centre near the shaft end; changing motor or wheel-face gap needs a fresh contact calculation. A parameter value satisfying the simple 4.5 mm engagement assertion does not itself establish adequate contact area.
- Verify ties, preload, torque reaction, axial retention and printed thin sections. The approximately 0.98 mm rear stop,1 mm tie-channel skin and 1.65 mm nut-cavity skin are intentional prototype details with untested load capacity; ties and captured fasteners must provide the actual retention.
- Freeze battery L/W/H/mass, exits and restraints; ESP/camera/ToF/driver/regulator board footprints, connectors, standoffs, wiring strain relief and switch access. Generic carriers do not certify PCB compatibility.
- The central base cable openings are covered by the installed battery floor. They are not an assembled through-wire route. Motor/electronics wiring should be routed above the tray/through the deck aperture, or use pack-specific protected exits once the harness is selected; aligned strap slots remain usable.
- Verify actual lens/ToF optical fields with the bumper, carrier, board and wiring installed. The 2 mm geometric aperture clearance is not an optical-field certification.
- Confirm fastener dimensions and torque, nut fit, ground clearance, printed tyre grip and load capacity. No slicer/G-code result, physical print, assembled spin test or load test is claimed here.
- Re-export and revalidate after parameter changes. Several board/support coordinates and tool-probe assumptions are explicit values for the default configuration; changing chassis, wheel, motor or carrier dimensions requires renewed mating, thin-wall, fastener-length and interference checks.

This review supports the corrected **generic CAD and conditional prototype exports**. It does not authorize treating unresolved component interfaces as frozen manufacturing drawings.

## USB-C charging cradle

The rear-right cradle and deck share two M3 holes at (27,28.5) and (51,28.5). The 3 mm floor seats on Z=41; a 39×18×6.3 mm module is reserved above Z=48, with 0.5 mm lateral clearance. Two underside 1.4 mm tie channels keep the installed deck clear of the retaining ties. The floor retains 1.6 mm above these 2.8 mm bridges and 1.3 mm outside the tie slots.

[Charger access checks](charger_access_results.json) pass the declared module envelope, rear 14×8×30 mm plug insertion path, vertical PCB lift, M3×10 hardware and pre-PCB tool access, and installed-deck tie routes. The 18 mm wide boot control collides as expected. [USB_C_CHARGING.md](../USB_C_CHARGING.md) records module selection, electrical requirements, printing and remaining actual-fit checks.

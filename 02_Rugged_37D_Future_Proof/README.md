# Rugged Future-Proof 4WD — Complete Parametric CAD

## Target
- Structural footprint: 360 x 290 mm
- 100 mm wheels
- 4WD differential drive
- 37D-class encoder motors
- Raspberry Pi 5
- ESP32-S3
- LiDAR-ready top deck
- modular sensor/payload mounting

## Structural design
Do not print the complete structural chassis as one plastic part. Use aluminium side rails/crossmembers or a thin aluminium base, then print the trays, brackets, mounts, bumper and sensor structures in PETG/ASA.

## Reference motor
The motor mount follows the published Pololu 37D family envelope: 37D gearbox, 6 mm output shaft and six M3 mounting holes in the gearbox face. Exact purchased motor dimensions must be verified before printing.

## Files
`rugged_rover_complete.scad` contains:
- side_rail()
- cross_member()
- electronics_tray()
- battery_tray()
- pi5_mount()
- esp32_mount()
- motor_mount()
- wheel_bearing_block()
- wheel()
- wheel_hub()
- camera_mount()
- tof_bracket()
- lidar_plate()
- lidar_mast()
- bumper()
- side_panel()
- assembly()

## Recommended printing
PETG or ASA, 0.2 mm layers, 5 perimeters, 35–50% infill.
Use metal motor brackets if possible.

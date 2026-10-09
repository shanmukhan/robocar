# Cute N20 4WD Rover — corrected assembled CAD

**Status:** corrected assembly layout; N20 motor interface remains generic until the exact motor is selected.

## Main design
- Chassis: 150 × 105 mm
- 4WD, four N20-class geared motors
- 45 mm wheels
- Wheel axes are horizontal across the chassis width and are coaxial with the motor shafts
- Lower battery tray
- Upper electronics deck on four standoffs
- ESP32 tray
- Front camera mount
- 3-position ToF sensor bar
- Front bumper
- M3 hardware throughout

## Important
This is a **parametric design**, not a final motor-specific production model. N20 motors sold by different vendors can have different gearbox lengths, shaft lengths, mounting features and body dimensions.

Before printing final motor mounts/hubs, select the exact N20 motor and update:
- `N20_BODY_L`
- `N20_BODY_W`
- `N20_BODY_H`
- `N20_SHAFT_D`
- `N20_GEARBOX_D`
- `N20_GEARBOX_L`

The complete SCAD now shows the rover as a physically assembled vehicle rather than an exploded arrangement.

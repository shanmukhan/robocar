# CAD research basis

## 37D motor reference
The geometry is based on published Pololu 37D metal gearmotor documentation:
- 37D gearbox family
- 6 mm output shaft
- six M3 mounting holes
- neighboring mounting holes 15.5 mm apart
- motor/gearbox diameter around 37 mm
- encoder versions add rear encoder hardware

Source:
https://www.pololu.com/product/2826
https://www.pololu.com/file/0J1735/37d-metal-gearmotors-dimension-diagram.pdf

## Why the N20 mount is generic
N20 is a family rather than a single standardized motor. Gearbox lengths, mounting holes, shafts and gear ratios vary by seller. Since the user has not purchased the motor yet, the CAD deliberately exposes the critical dimensions rather than hard-coding an unverified seller-specific motor.

## Print strategy
For the small rover, PETG is preferred.
For the rugged rover, use PETG or ASA for printed modules and aluminium/metal for the primary load-bearing structure.

## Do not print final production parts yet
The exact motor, wheel hub and battery dimensions must be frozen first.

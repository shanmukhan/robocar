# Rugged & Smart 4WD Rover

**Project status:** Architecture/BOM/CAD planning; not physically built yet  
**Document date:** 2026-10-03

## 1. Purpose

A larger 4WD rover for **tile, dirt/soil, small stones, grass and slopes**, with a target structural footprint around **360 × 290 mm**.

The key architecture is:

- **Raspberry Pi 5:** ROS 2, LiDAR, SLAM, camera, navigation and high-level autonomy
- **ESP32-S3:** real-time motor control, encoder capture, PID and safety
- **4 × JGB37-520 12 V 60 RPM AB-encoder motors**
- **100 mm wheels**
- **12.8 V LiFePO4 battery**
- LiDAR-ready upper deck

![Rugged rover concept](rugged_rover_top.svg)

## 2. Mechanical architecture

The main structural load-bearing frame should preferably use:

- aluminium rails/plates
- aluminium motor plates
- printed PETG/ASA brackets, trays, covers and guards

Avoid making one huge 360 × 290 mm structural slab entirely from 3D print material.

## 3. Selected motor

**4 × JGB37-520, 12 V, 60 RPM, AB quadrature encoder**

EngineersToy's current listing specifies:

- DC 6–12 V
- 6 mm D-shaped shaft
- 21 mm shaft length
- AB dual-phase encoder
- 11-wire encoder
- encoder signal voltage 3.3 V or 5 V
- selectable 10/60/100/200 RPM variants
- listing range ₹135–₹595 depending on selected variant/options

Source: https://www.engineerstoy.com/product/dc-geared-motor-with-encoder-jgb37-520-12v/

**Important:** torque, stall current and exact mounting geometry for the selected 60 RPM variant must be confirmed before final driver/fuse/CAD sizing.

## 4. Speed calculation

For 100 mm wheels:

```text
Circumference = π × 0.1 ≈ 0.314 m

60 RPM:
0.314 × 60 / 60 ≈ 0.314 m/s
≈ 1.13 km/h theoretical
```

At 100 RPM the same wheel gives about 1.88 km/h theoretical.

Actual loaded speed will be lower.

## 5. Encoder architecture

Each motor provides AB quadrature:

```text
Motor 1 -> A/B
Motor 2 -> A/B
Motor 3 -> A/B
Motor 4 -> A/B
```

That is **8 encoder signal inputs**.

Benefits:

- direction
- wheel speed
- closed-loop velocity
- odometry
- later slip detection

The exact encoder CPR must be obtained from the selected motor datasheet or measured experimentally.

## 6. Control architecture

```text
             Phone / UI
                 |
               Wi-Fi
                 |
        +--------v---------+
        | Raspberry Pi 5  |
        | ROS 2 / LiDAR   |
        | Vision / SLAM   |
        +--------+--------+
                 |
              USB/UART
                 |
        +--------v--------+
        | ESP32-S3        |
        | PID + Encoders  |
        | PWM + Safety    |
        +----+--------+---+
             |        |
        Driver A   Driver B
          |  |       |  |
         LF LR      RF RR
```

**Preferred:** Pi ↔ ESP32 over USB/UART for deterministic control. Wi-Fi is for phone/high-level control and telemetry. Safety must not depend on Wi-Fi.

## 7. Motor drivers

Use **two high-current dual-channel motor drivers** or an equivalent 4-channel architecture.

Earlier discussion used roughly **15 A or more peak per channel as a design guideline**, but this is not a final specification. Recalculate from the exact JGB37-520 60 RPM stall current.

Do not size a driver from nominal running current only.

## 8. Battery

Baseline:

**12.8 V 15 Ah LiFePO4**

Nominal energy:

```text
12.8 × 15 = 192 Wh
```

Robu currently lists the Pro-Range IFR 32140FS 12.8 V 15 Ah 2C 4S1P pack at about **₹3,519**.

Source: https://robu.in/product/4s1p-lifepo4-battery-pack/

The exact pack's discharge capability and BMS inclusion must be verified before ordering.

## 9. BMS

BMS current rating must be coordinated with:

- motor stall current
- motor driver limits
- battery-cell discharge capability
- fuse
- cable gauge

Options discussed:

### 4S 20 A LFP BMS

MakerBazar:

- 4S / 12.8 V
- 20 A
- explicitly LiFePO4
- temperature sensor
- approx. ₹249

https://makerbazar.in/products/12-8v-bms-4s-20a-32650-lithium-battery-protection-board-only-for-lifepo4

### JBD 4S LFP family

MakerBazar lists 30/40/50/60 A variants:

https://makerbazar.in/products/jiabaida-jbd-normal-bms-4s-12v-lifepo4

### TDT 50 A

Robu lists a 4S 12.8 V 50 A smart LFP BMS with passive balancing and temperature monitoring; it was out of stock when checked:

https://robu.in/product/tdt-lifepo4-lfp-4s-12-8v-50a-2/

For this rover, do not automatically select 20 A or 50 A. Match the BMS to the final motor/current measurements.

## 10. Charger

Target:

**14.6 V, 5 A LiFePO4 CC/CV charger**

A current product result showed a Quartz Components 14.6 V 5 A LiFePO4 charger around ₹2,394.

A Robu 14.5 V 5 A 4S LiFePO4 charger was also found around ₹1,979. Verify the exact charge-voltage specification before purchase.

**Never use a normal 4S Li-ion 16.8 V charger for a 4S LiFePO4 pack.**

## 11. Power system

```text
12.8 V LiFePO4
      |
     BMS
      |
   Main fuse
      |
 Main switch
      |
 Power distribution
   /          motors       DC-DC
              |
             5 V
              |
       Raspberry Pi 5
```

The Pi must not be connected directly to the 12.8 V battery.

## 12. Raspberry Pi 5

Official Raspberry Pi documentation specifies:

- BCM2712 2.4 GHz quad-core Arm CPU
- Wi-Fi
- Bluetooth
- USB 3
- Gigabit Ethernet
- MIPI camera/display interfaces
- PCIe 2.0 x1
- 5 V / 5 A USB-C power

Official source: https://www.raspberrypi.com/products/raspberry-pi-5/

Use active cooling for sustained workloads.

## 13. Pi power

Use a quality regulated **5 V high-current DC-DC converter** with enough transient margin for the Pi, USB devices, camera and LiDAR.

A weak buck converter can cause:

- brownouts
- USB disconnects
- camera failures
- LiDAR instability
- ROS node failures

## 14. Sensors

### Camera

For:

- live video
- object detection
- visual navigation
- recording

### IMU

For:

- gyro
- acceleration
- orientation
- sensor fusion

### ToF

For short-range obstacle detection.

### LiDAR

Future primary sensor for:

- 2D mapping
- obstacle detection
- SLAM
- autonomous navigation

Reserve a vibration-conscious top mount.

## 15. Wheel design

Baseline:

- 4 × 100 mm wheels
- tread suitable for grass/soil
- 6 mm D-shaft compatible hub
- exact wheel bore and offset to be frozen with the selected motor

For rough terrain, avoid putting excessive radial/side load on the gearbox shaft. Consider bearing support if the wheel is heavy.

## 16. Chassis

Target:

**360 × 290 mm class**

Suggested stack:

```text
LiDAR / camera
      |
sensor deck
      |
Pi + ESP32 + power
      |
aluminium frame
      |
motor plates
      |
100 mm wheels
```

## 17. Encoder wiring

The selected motor has an 11-wire encoder harness. Before wiring, identify:

- motor +
- motor -
- encoder VCC
- encoder GND
- encoder A
- encoder B

Do not guess the remaining wires.

Verify the encoder's actual output voltage before connecting it directly to ESP32-S3 GPIO.

## 18. Firmware

ESP32:

```text
Encoder capture
      |
speed estimator
      |
PID controller
      |
PWM
      |
motor driver
```

Command path:

```text
Pi
 |
USB/UART
 |
command parser
 |
target wheel speeds
 |
4 × PID loops
```

Safety:

```text
No command for N ms
        |
       STOP
```

## 19. Differential-drive equations

For left/right wheel groups:

```text
V_left  = V - ωL/2
V_right = V + ωL/2
```

Then:

```text
RPM = Vwheel × 60 / (π × wheel_diameter)
```

For a 100 mm wheel:

```text
RPM ≈ Vwheel × 190.99
```

when Vwheel is in m/s.

## 20. ROS 2 architecture

```text
Pi 5
 |
 +-- ROS 2
 |   +-- cmd_vel
 |   +-- odometry
 |   +-- TF
 |   +-- LiDAR
 |   +-- camera
 |   +-- IMU
 |   +-- SLAM
 |   +-- Nav2
 |
 +-- ESP32 bridge
        |
       USB/UART
```

## 21. Rugged rover BOM

| Qty | Item | Target |
|---:|---|---|
| 4 | JGB37-520 motors | 12 V, 60 RPM, AB encoder |
| 4 | Wheels | 100 mm, 6 mm D-bore |
| 2 | Dual motor drivers | High-current; size after stall-current test |
| 1 | Raspberry Pi 5 | 8 GB preferred for heavier vision/ROS use |
| 1 | ESP32-S3 | Real-time controller |
| 1 | LiFePO4 battery | 12.8 V, 15 Ah baseline |
| 1 | LFP BMS | 4S; current matched to pack/motors |
| 1 | LFP charger | 14.6 V, 5 A CC/CV |
| 1 | DC-DC converter | 12.8 V → regulated 5 V, high current |
| 1 | Main fuse | Final rating after measured current |
| 1 | Main switch | DC/high-current rated |
| 1 | Power distribution | High-current terminals |
| 1 | IMU | I²C/SPI |
| 1 | Camera | CSI/USB/ESP32-S3 option |
| 1 | LiDAR | 2D baseline, future |
| 1–3 | ToF | Short-range sensing |
| 1 | Pi active cooler | Required for sustained compute |
| 1 | microSD | Reliable/high-endurance |
| 1 set | Aluminium frame/plates | Structural |
| 1 set | PETG/ASA printed modules | Trays/brackets/covers |
| 1 set | M3/M4 fasteners | Lock nuts preferred |
| 1 set | Power/signal wiring | Properly sized |
| 1 set | XT60/XT90/connectors | Main battery path |

## 22. Runtime

Battery energy is approximately:

`12.8 V × 15 Ah = 192 Wh`.

Actual runtime depends on motor load, terrain, duty cycle, Pi/LiDAR/camera consumption and converter efficiency.

Example only:

`192 Wh / 60 W ≈ 3.2 hours theoretical`.

Do not treat that as a guaranteed runtime.

## 23. Safety checklist

Before connecting the battery:

- verify polarity
- verify BMS wiring
- verify 4S LFP chemistry
- verify 14.6 V charger
- install fuse
- use correct cable gauge
- insulate exposed terminals
- secure battery mechanically
- protect wires from moving wheels
- verify 5 V rail before Pi connection
- verify encoder electrical levels
- add an accessible emergency stop

## 24. Build sequence

### Phase 1 — Mechanical

1. Buy one JGB37-520 60 RPM motor first if possible.
2. Measure gearbox.
3. Measure shaft and mounting holes.
4. Select wheel.
5. Design motor plate.
6. Fit-test printed mount.
7. Verify ground clearance.

### Phase 2 — Power

1. Select battery.
2. Confirm cell discharge capability.
3. Select BMS.
4. Select fuse.
5. Select driver.
6. Build protected power distribution.
7. Test 5 V DC-DC independently.

### Phase 3 — ESP32

1. Read one encoder.
2. Drive one motor.
3. Implement direction.
4. Implement PWM.
5. Implement PID.
6. Add all four motors.
7. Add watchdog.
8. Add Pi communication.

### Phase 4 — Pi/ROS 2

1. Install OS.
2. Install ROS 2.
3. Connect ESP32.
4. Publish wheel odometry.
5. Add IMU.
6. Add camera.
7. Add LiDAR.
8. Add SLAM.
9. Add Nav2.

### Phase 5 — Terrain

Test progressively:

1. tile
2. carpet
3. soil
4. small stones
5. grass
6. slopes

Record motor/driver temperature, current, wheel slip, battery voltage and encoder reliability.

## 25. CAD freeze checklist

Final CAD must verify:

- exact JGB37-520 60 RPM motor body
- mounting-hole pattern
- 6 mm D shaft
- 21 mm shaft length
- wheel bore
- wheel width
- wheel offset
- ground clearance
- battery dimensions
- Pi mounting
- driver mounting
- cable exits
- LiDAR height
- camera field of view

Earlier CAD iterations showed floating/exploded wheel placement. The final design must be assembled around real mechanical constraints rather than relying on a concept render.

## 26. Future upgrades

- calibrated encoder CPR
- IMU sensor fusion
- wheel-slip detection
- ROS 2 Nav2
- LiDAR SLAM
- camera object detection
- autonomous waypoints
- GPS/RTK
- current/voltage telemetry
- emergency-stop button
- motor temperature sensors
- suspension

## 27. Key sources

- EngineersToy JGB37-520 encoder motor: https://www.engineerstoy.com/product/dc-geared-motor-with-encoder-jgb37-520-12v/
- Robu 12.8 V 15 Ah LiFePO4: https://robu.in/product/4s1p-lifepo4-battery-pack/
- Robu LiFePO4 category: https://robu.in/product-category/12v-12-8v14-6v/
- MakerBazar 4S 20 A LFP BMS: https://makerbazar.in/products/12-8v-bms-4s-20a-32650-lithium-battery-protection-board-only-for-lifepo4
- MakerBazar JBD 4S LFP BMS: https://makerbazar.in/products/jiabaida-jbd-normal-bms-4s-12v-lifepo4
- Robu TDT 50 A LFP BMS: https://robu.in/product/tdt-lifepo4-lfp-4s-12-8v-50a-2/
- Raspberry Pi 5: https://www.raspberrypi.com/products/raspberry-pi-5/

**Price note:** prices are snapshots checked around 2026-10-03 and can change with stock, variant, GST and shipping.

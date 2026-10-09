// ============================================================
// Cute N20 4WD Rover - corrected assembled parametric CAD
// Units: mm
// NOTE: N20 motor interface is intentionally generic until the
// exact motor is selected. The visual assembly is mechanically
// arranged as a real 4WD rover: wheels coaxial with motor shafts.
// ============================================================

$fn = 48;

// ---------- Main dimensions ----------
CHASSIS_L = 150;              // X: front/rear
CHASSIS_W = 105;              // Y: left/right
BASE_T = 4;

WHEEL_D = 45;
WHEEL_W = 14;
WHEEL_BORE = 3.2;
WHEEL_HUB_D = 14;

// Generic N20 envelope. Confirm against the motor actually purchased.
N20_BODY_L = 25;              // motor length along shaft axis
N20_BODY_W = 12;              // cross-section Y/Z
N20_BODY_H = 10;
N20_SHAFT_D = 3;
N20_GEARBOX_D = 12;
N20_GEARBOX_L = 6;

M3 = 3.2;

// Wheel/motor positions
WHEEL_X = 52;
SIDE_Y = CHASSIS_W/2 + WHEEL_W/2 - 1; // wheel center Y
SHAFT_Z = BASE_T + WHEEL_D/2;         // 26.5 mm

// Upper deck
DECK_L = 120;
DECK_W = 76;
DECK_T = 3;
DECK_Z = 38;
STAND_D = 8;
STAND_H = DECK_Z - BASE_T - 2;

// ---------- Utility ----------
module rounded_box(x,y,z,r=3,center=false) {
    if (center) {
        translate([-x/2,-y/2,0])
            hull() {
                for (xx=[r,x-r], yy=[r,y-r])
                    translate([xx,yy,0]) cylinder(r=r,h=z);
            }
    } else {
        hull() {
            for (xx=[r,x-r], yy=[r,y-r])
                translate([xx,yy,0]) cylinder(r=r,h=z);
        }
    }
}

// ---------- Base plate ----------
module base_plate() {
    difference() {
        translate([0,0,BASE_T/2])
            rounded_box(CHASSIS_L, CHASSIS_W, BASE_T, 5, true);

        // General M3 mounting grid, kept away from motor perimeter.
        for (x=[-60,-30,0,30,60])
            for (y=[-35,0,35])
                translate([x,y,-1]) cylinder(d=M3,h=BASE_T+2);

        // Lightweight cable slots through the central area.
        for (x=[-20,0,20])
            translate([x,0,-1]) cube([8,24,BASE_T+2],center=true);
    }
}

// ---------- Motor mount ----------
// One mount per motor. Axis is Y, so the output shaft points outward
// through the left/right side of the chassis. The same part is mirrored
// by the assembly for the opposite side.
module n20_motor_mount() {
    // A compact side bracket with an adjustable motor cavity.
    difference() {
        translate([-15,-10,BASE_T])
            rounded_box(30,20,25,3,false);

        // Motor body cavity, axis along Y.
        translate([0,0,SHAFT_Z])
            rotate([90,0,0])
                cylinder(d=N20_BODY_W+1.2,h=22,center=true);

        // Gearbox/shaft clearance through the side wall.
        translate([0,0,SHAFT_Z])
            rotate([90,0,0])
                cylinder(d=N20_GEARBOX_D+1.5,h=30,center=true);

        // Open the inner side so the motor can slide into the bracket.
        translate([-8,-11,BASE_T+12])
            cube([16,22,16],center=true);

        // Two M3 mounting holes through the bottom flange.
        for (x=[-10,10])
            translate([x,0,BASE_T-1])
                cylinder(d=M3,h=7);
    }
}

// ---------- Motor visual placeholder ----------
// Visual-only. Shaft axis = Y.
module n20_motor_placeholder(outward=1) {
    color("silver") {
        // Motor can, axis along Y.
        rotate([90,0,0])
            cylinder(d=N20_BODY_W,h=N20_BODY_L,center=true);

        // Gearbox and shaft are on the OUTWARD side.
        translate([0,outward*(N20_BODY_L/2+N20_GEARBOX_L/2),0])
            rotate([90,0,0])
                cylinder(d=N20_GEARBOX_D,h=N20_GEARBOX_L,center=true);

        translate([0,outward*(N20_BODY_L/2+N20_GEARBOX_L+4),0])
            rotate([90,0,0])
                cylinder(d=N20_SHAFT_D,h=8,center=true);
    }
}

// ---------- Wheel ----------
module wheel() {
    difference() {
        union() {
            cylinder(d=WHEEL_D,h=WHEEL_W,center=true);
            // raised center hub
            cylinder(d=WHEEL_HUB_D+4,h=WHEEL_W+2,center=true);
        }

        cylinder(d=WHEEL_BORE,h=WHEEL_W+5,center=true);

        // Six simple tread grooves.
        for (a=[0:30:330])
            rotate([0,0,a])
                translate([WHEEL_D/2-2,0,0])
                    cube([4,3,WHEEL_W+4],center=true);
    }
}

// ---------- Wheel hub adapter ----------
module wheel_hub_adapter() {
    difference() {
        cylinder(d=WHEEL_HUB_D,h=10,center=true);
        cylinder(d=N20_SHAFT_D+0.25,h=12,center=true);
        translate([0,0,0]) cube([1.2,WHEEL_HUB_D+2,12],center=true);
        for (a=[0,180])
            rotate([0,0,a])
                translate([5,0,0]) cylinder(d=M3,h=12,center=true);
    }
}

// ---------- Battery tray ----------
module battery_tray() {
    difference() {
        rounded_box(72,42,7,4,true);
        translate([0,0,3]) cube([62,32,8],center=true);
        for (x=[-29,29], y=[-15,15])
            translate([x,y,-1]) cylinder(d=M3,h=10);
    }
}

// ---------- ESP32 tray ----------
module esp32_tray() {
    difference() {
        rounded_box(58,32,6,4,true);
        for (x=[-23,23], y=[-12,12])
            translate([x,y,-1]) cylinder(d=M3,h=10);
    }
}

// ---------- Camera mount ----------
module camera_mount() {
    difference() {
        rounded_box(36,24,8,4,true);
        for (x=[-12,12])
            translate([x,0,-1]) cylinder(d=M3,h=12);
        translate([0,-1,4]) cube([20,8,10],center=true);
    }
}

// ---------- ToF sensor bar ----------
module tof_sensor_bar() {
    difference() {
        rounded_box(86,14,8,3,true);
        for (x=[-32,0,32])
            translate([x,0,-1]) cylinder(d=8,h=12);
        for (x=[-40,40])
            translate([x,0,-1]) cylinder(d=M3,h=12);
    }
}

// ---------- Upper electronics deck ----------
module top_deck() {
    difference() {
        translate([0,0,DECK_Z])
            rounded_box(DECK_L,DECK_W,DECK_T,5,true);

        // central cable opening
        translate([0,0,DECK_Z-1])
            cube([45,30,DECK_T+2],center=true);

        // corner standoff holes
        for (x=[-50,50], y=[-30,30])
            translate([x,y,DECK_Z-1]) cylinder(d=M3,h=DECK_T+2);
    }
}

// ---------- Standoffs ----------
module standoffs() {
    for (x=[-50,50], y=[-30,30]) {
        translate([x,y,BASE_T])
            difference() {
                cylinder(d=STAND_D,h=STAND_H);
                translate([0,0,-1]) cylinder(d=M3,h=STAND_H+2);
            }
    }
}

// ---------- Front camera plate ----------
module camera_front_mount() {
    // Front = -Y. This plate is fixed to the front edge of the deck.
    translate([0,-DECK_W/2-2,DECK_Z+2])
        difference() {
            rounded_box(44,6,26,3,true);
            translate([0,0,13]) cube([22,8,12],center=true);
            for (x=[-16,16])
                translate([x,0,3]) rotate([90,0,0]) cylinder(d=M3,h=10,center=true);
        }
}

// ---------- Legacy top-cover alias ----------
// Kept so the individual top_cover.scad wrapper remains valid.
module top_cover() { top_deck(); }

// ---------- Front bumper ----------
module front_bumper() {
    translate([0,-CHASSIS_W/2-5,10])
        difference() {
            rounded_box(120,8,16,4,true);
            for (x=[-45,-30,-15,0,15,30,45])
                translate([x,0,-1]) cylinder(d=M3,h=20);
        }
}

// ---------- Complete assembled rover ----------
module assembly(show_motors=true, show_wheels=true, show_deck=true) {
    // Chassis
    color("gold") base_plate();

    // Four motor brackets, two on each side. They are attached to the
    // chassis perimeter and centered at the wheel shaft height.
    for (sx=[-1,1], sy=[-1,1]) {
        x = sx*WHEEL_X;
        y = sy*(CHASSIS_W/2-10);

        translate([x,y,0]) n20_motor_mount();

        if (show_motors)
            translate([x,y,SHAFT_Z])
                n20_motor_placeholder(sy);

        if (show_wheels)
            translate([x,sy*SIDE_Y,SHAFT_Z])
                rotate([90,0,0]) wheel();
    }

    // Low-mounted battery tray.
    color("orange")
        translate([0,10,BASE_T+2]) battery_tray();

    // Upper electronics deck and four real mounting standoffs.
    if (show_deck) {
        color("gold") standoffs();
        color("gold") top_deck();

        color("orange")
            translate([22,12,DECK_Z+DECK_T]) esp32_tray();
    }

    // Front sensing/camera hardware.
    color("orange")
        translate([0,-CHASSIS_W/2+4,BASE_T+2]) tof_sensor_bar();

    color("orange")
        translate([0,-DECK_W/2+10,DECK_Z+DECK_T+1]) camera_mount();

    // Front bumper is at -Y.
    color("gold") front_bumper();
}

assembly();

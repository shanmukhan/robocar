
// ============================================================
// Rugged Future-Proof 4WD Rover - complete parametric CAD
// Units: mm
// Reference motor: Pololu 37D 12V encoder class.
// Exact motor dimensions are parameterized around the published
// 37D family; verify the purchased motor before printing mounts.
// Structural chassis intentionally uses aluminium rails/plates.
// Printed modules are PETG/ASA.
// ============================================================

$fn = 72;

// ---------- Main dimensions ----------
BASE_L = 360;
BASE_W = 290;
BASE_T = 5;

WHEEL_D = 100;
WHEEL_W = 32;
WHEEL_BORE = 6.2;

MOTOR_D = 37.0;
MOTOR_FACE_D = 36.8;
MOTOR_SHAFT_D = 6.0;
MOTOR_FACE_HOLE_CIRCLE_R = 17.9; // approximate hex-pattern radius
MOTOR_HOLE_NEIGHBOR = 15.5;

M3 = 3.4;
M4 = 4.4;

// ---------- Utilities ----------
module rounded_box(x,y,z,r=5,center=false) {
    if (center)
        translate([-x/2,-y/2,0])
            hull() {
                for (xx=[r,x-r], yy=[r,y-r])
                    translate([xx,yy,0]) cylinder(r=r,h=z);
            }
    else
        hull() {
            for (xx=[r,x-r], yy=[r,y-r])
                translate([xx,yy,0]) cylinder(r=r,h=z);
        }
}

// ---------- Structural rail ----------
module side_rail() {
    difference() {
        rounded_box(330,28,24,6,center=true);

        for (x=[-140,-120,-100,-80,-60,-40,-20,0,20,40,60,80,100,120,140])
            translate([x,0,-1])
                cylinder(d=M4,h=30);
    }
}

// ---------- Cross member ----------
module cross_member() {
    difference() {
        rounded_box(250,24,24,5,center=true);
        for (x=[-100,-80,-60,-40,-20,0,20,40,60,80,100])
            translate([x,0,-1])
                cylinder(d=M4,h=30);
    }
}

// ---------- Electronics tray ----------
module electronics_tray() {
    difference() {
        rounded_box(205,135,8,8,center=true);

        for (x=[-80,-60,-40,-20,0,20,40,60,80])
            for (y=[-40,-20,0,20,40])
                translate([x,y,-1])
                    cylinder(d=M3,h=12);

        // cable channels
        for (x=[-75,75])
            translate([x,0,-1])
                cube([14,80,12],center=true);
    }
}

// ---------- Battery tray ----------
module battery_tray() {
    difference() {
        rounded_box(220,100,12,8,center=true);
        cube([200,80,16],center=true);

        for (x=[-95,95])
            for (y=[-35,35])
                translate([x,y,-1])
                    cylinder(d=M4,h=20);
    }
}

// ---------- Pi 5 mount ----------
module pi5_mount() {
    difference() {
        rounded_box(90,70,8,5,center=true);

        // Pi 5 mounting hole pattern, 58 x 49 mm nominal
        for (x=[-29,29])
            for (y=[-24.5,24.5])
                translate([x,y,-1])
                    cylinder(d=M3,h=12);

        // ventilation opening
        translate([0,0,-1])
            cube([50,30,12],center=true);
    }
}

// ---------- ESP32 tray ----------
module esp32_mount() {
    difference() {
        rounded_box(65,42,6,4,center=true);
        for (x=[-25,25])
            for (y=[-15,15])
                translate([x,y,-1])
                    cylinder(d=M3,h=10);
    }
}

// ---------- Generic 37D motor plate ----------
module motor_mount() {
    // Plate bolts to chassis; motor bolts to plate through six-hole
    // hexagonal pattern. Adjust hole radius if exact motor differs.
    difference() {
        rounded_box(62,62,8,6,center=true);

        // motor face clearance
        translate([0,0,-1])
            cylinder(d=30,h=12);

        // six M3 mounting holes
        for (a=[0:60:300])
            translate([MOTOR_FACE_HOLE_CIRCLE_R*cos(a),
                       MOTOR_FACE_HOLE_CIRCLE_R*sin(a),-1])
                cylinder(d=M3,h=12);

        // chassis mounting holes
        for (x=[-22,22])
            for (y=[-22,22])
                translate([x,y,-1])
                    cylinder(d=M4,h=12);
    }
}

// ---------- Bearing block ----------
module wheel_bearing_block() {
    difference() {
        rounded_box(45,45,16,6,center=true);
        translate([0,0,-1])
            cylinder(d=22,h=20);
        for (x=[-15,15])
            for (y=[-15,15])
                translate([x,y,-1])
                    cylinder(d=M4,h=20);
    }
}

// ---------- 100 mm wheel ----------
module wheel() {
    difference() {
        cylinder(d=WHEEL_D,h=WHEEL_W,center=true);
        cylinder(d=WHEEL_BORE,h=WHEEL_W+2,center=true);

        // aggressive tread slots
        for (a=[0:20:340])
            rotate([0,0,a])
                translate([WHEEL_D/2-5,0,0])
                    rotate([0,15,0])
                        cube([8,5,WHEEL_W+2],center=true);
    }
}

// ---------- 6 mm D-shaft wheel hub ----------
module wheel_hub() {
    difference() {
        cylinder(d=42,h=20,center=true);

        // shaft bore (round baseline; add D-flat manually in CAD if needed)
        cylinder(d=MOTOR_SHAFT_D+0.15,h=24,center=true);

        // four wheel fasteners
        for (a=[45:90:360])
            translate([15*cos(a),15*sin(a),0])
                cylinder(d=M4,h=24,center=true);
    }
}

// ---------- Camera mount ----------
module camera_mount() {
    difference() {
        rounded_box(70,40,10,6,center=true);
        for (x=[-25,25])
            translate([x,0,-1])
                cylinder(d=M3,h=14);
        translate([0,0,5])
            cube([36,8,12],center=true);
    }
}

// ---------- 3x ToF bracket ----------
module tof_bracket() {
    difference() {
        rounded_box(140,18,12,4,center=true);

        for (x=[-50,0,50])
            translate([x,0,-1])
                cylinder(d=8,h=16);

        for (x=[-65,65])
            translate([x,0,-1])
                cylinder(d=M4,h=16);
    }
}

// ---------- LiDAR plate ----------
module lidar_plate() {
    difference() {
        rounded_box(110,110,8,8,center=true);

        for (x=[-40,-20,0,20,40])
            for (y=[-40,-20,0,20,40])
                translate([x,y,-1])
                    cylinder(d=M3,h=12);

        translate([0,0,-1])
            cylinder(d=22,h=12);
    }
}

// ---------- LiDAR mast ----------
module lidar_mast() {
    difference() {
        rounded_box(38,38,120,6,center=true);

        // central cable passage
        translate([0,0,-1])
            cylinder(d=14,h=125,center=true);

        for (x=[-12,12])
            for (y=[-12,12])
                translate([x,y,-1])
                    cylinder(d=M3,h=20);
    }
}

// ---------- Front/rear bumper ----------
module bumper() {
    difference() {
        rounded_box(330,24,28,7,center=true);

        for (x=[-140,-120,-100,-80,-60,-40,-20,0,20,40,60,80,100,120,140])
            translate([x,0,-1])
                cylinder(d=M4,h=32);
    }
}

// ---------- Side body panel ----------
module side_panel() {
    difference() {
        rounded_box(330,5,90,5,center=true);
        for (x=[-140,-120,-100,-80,-60,-40,0,40,60,80,100,120,140])
            translate([x,0,0])
                rotate([90,0,0])
                    cylinder(d=M4,h=10,center=true);
    }
}

// ---------- Generic motor visual ----------
module motor_placeholder() {
    color("silver")
        cylinder(d=MOTOR_D,h=65,center=true);
    color("gray")
        translate([0,0,35])
            cylinder(d=MOTOR_FACE_D,h=26.5,center=true);
    color("black")
        translate([0,0,50])
            cylinder(d=MOTOR_SHAFT_D,h=16,center=true);
}

// ---------- Complete assembly preview ----------
module assembly() {
    // rails
    color("gray") {
        translate([0,-125,0]) side_rail();
        translate([0, 125,0]) side_rail();
        translate([0,-55,0]) cross_member();
        translate([0, 55,0]) cross_member();
    }

    // electronics
    translate([0,0,35]) electronics_tray();
    translate([0,0,48]) battery_tray();
    translate([-55,0,60]) pi5_mount();
    translate([55,0,60]) esp32_mount();

    // sensor modules
    translate([0,-155,55]) camera_mount();
    translate([0,-160,35]) tof_bracket();

    // LiDAR
    translate([0,0,105]) lidar_plate();
    translate([0,0,160]) lidar_mast();

    // bumpers
    translate([0,-150,20]) bumper();
    translate([0,150,20]) bumper();

    // wheels
    for (sx=[-1,1], sy=[-1,1])
        translate([sx*150,sy*150,50])
            rotate([90,0,0])
                wheel();
}

// ---------- Default preview ----------
assembly();

// Individual export examples:
// side_rail();
// cross_member();
// electronics_tray();
// battery_tray();
// pi5_mount();
// esp32_mount();
// motor_mount();
// wheel_bearing_block();
// wheel();
// wheel_hub();
// camera_mount();
// tof_bracket();
// lidar_plate();
// lidar_mast();
// bumper();
// side_panel();

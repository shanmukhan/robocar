// Cute N20 4WD: audited PARAMETRIC PROTOTYPE, units mm.
// Exact motor, battery, PCB footprints and printer fit remain UNVERIFIED.
// X longitudinal (front=-X), Y axle, base underside Z=0.
// Printable modules start at Z=0; assembly() applies placements.
$fn=96;
EPS=0.02;
CHASSIS_L=150;
CHASSIS_W=105;
BASE_T=4;
GROUND_CLEARANCE=5;             // project target above nominal tyre plane
WHEEL_D=45;
WHEEL_W=14;
WHEEL_HUB_D=14;
HUB_FLANGE_D=30;
HUB_FLANGE_H=9;
HUB_H=10;
HUB_BOLT_R=9;
HUB_BOLT_ANGLES=[90,210,330];
HUB_SET_ANGLE=30;               // free sector between axial bolts
HUB_POCKET_CLEARANCE=0.4;       // diametral prototype fit allowance
WHEEL_BORE=3.4;
// ORIGINAL GENERIC envelopes, not a selected motor SKU.
// BODY_L excludes gearbox: measure actual can and gearbox separately.
N20_BODY_L=25;
N20_BODY_W=12;
N20_BODY_H=10;
N20_SHAFT_D=3;
N20_SHAFT_L=8;                 // original placeholder, NOT a datasheet value
N20_GEARBOX_D=12;              // legacy parameter: conservative square envelope
N20_GEARBOX_W=N20_GEARBOX_D;
N20_GEARBOX_H=N20_GEARBOX_D;
N20_GEARBOX_L=6;
MOTOR_SIDE_CLEARANCE=0.3;      // each side; floor is supporting datum
MOTOR_FACE_Y=CHASSIS_W/2;
WHEEL_FACE_GAP=2;
SIDE_Y=MOTOR_FACE_Y+WHEEL_FACE_GAP+WHEEL_W/2;
SHAFT_Z=WHEEL_D/2-GROUND_CLEARANCE;
WHEEL_X=52;
SHAFT_ENGAGEMENT=min(HUB_H,N20_SHAFT_L-WHEEL_FACE_GAP);
// Hardware allowances: measure hardware and print fit coupon.
M3=3.4;
M3_HEAD_D=6.6;
M3_NUT_AF=5.7;
M3_NUT_H=2.7;
MOUNT_FOOT_X=12;
MOUNT_FOOT_Y=-(N20_BODY_L+N20_GEARBOX_L)/2;
MOUNT_W=32;
MOUNT_T=3;
MOUNT_AXIS_Z=SHAFT_Z-BASE_T;
MOUNT_TOP=MOUNT_AXIS_Z+min(N20_BODY_H,N20_GEARBOX_H)/2-2;
DECK_L=120;
DECK_W=76;
DECK_T=3;
DECK_Z=38;
STAND_D=8;
STAND_H=DECK_Z-BASE_T;
STAND_POINTS=[for(x=[-50,50],y=[-14,14]) [x,y]];
BATTERY_L=62;                 // cavity, NOT selected battery dimensions
BATTERY_W=32;
BATTERY_FLOOR=2.4;
BATTERY_RIM_H=7;
BATTERY_POINTS=[for(x=[-40,40],y=[-10,10]) [x,y]];
ESP_POS=[16,0];
ESP_POINTS=[for(x=[-23,23],y=[-10,10]) [x,y]];
CAMERA_POS=[-48,0];
CAMERA_POINTS=[[-2,-14],[-2,14],[8,-10],[8,10]];
TOF_POS=[-80,0];
TOF_POINTS=[[11,-12],[11,12]];
BUMPER_POS=[-87,0];
BUMPER_POINTS=[[16,0],[24,0]];
assert(GROUND_CLEARANCE>0 && SHAFT_Z>BASE_T+max(N20_BODY_H,N20_GEARBOX_H)/2);
assert(STAND_H>0 && DECK_Z>BASE_T+MOUNT_TOP);
assert(SHAFT_ENGAGEMENT>=4.5,"Generic shaft engagement too short: measure motor/hub");
assert(MOUNT_W/2>MOUNT_FOOT_X+M3/2+2);
assert(HUB_FLANGE_D/2>HUB_BOLT_R+M3_NUT_AF/sqrt(3)+2);
assert(WHEEL_FACE_GAP>1.5,"Wheel must clear saddle nose");
assert(HUB_H<WHEEL_W && HUB_FLANGE_H<HUB_H);
assert(min(N20_BODY_H,N20_GEARBOX_H)>=8,"Check tie contact and saddle sidewall height");
// center means XY-centred, never Z-centred.
module rounded_box(x,y,z,r=3,center=false) {
    assert(x>=2*r && y>=2*r && z>0 && r>0);
    translate(center?[-x/2,-y/2,0]:[0,0,0])
        hull() for(xx=[r,x-r],yy=[r,y-r])
            translate([xx,yy,0]) cylinder(r=r,h=z);
}
module hole_z(p,h,d=M3) {
    translate([p[0],p[1],-EPS]) cylinder(d=d,h=h+2*EPS);
}
module hex_nut(h=M3_NUT_H) { cylinder(r=M3_NUT_AF/sqrt(3),h=h,$fn=6); }
module side_placement(sx,sy) {
    translate([sx*WHEEL_X,sy*MOTOR_FACE_Y,BASE_T])
        if(sy==1) children(); else mirror([0,1,0]) children();
}
module axle_placement(sx,sy) {
    translate([sx*WHEEL_X,sy*(MOTOR_FACE_Y+WHEEL_FACE_GAP),SHAFT_Z])
        rotate([sy==-1?90:-90,0,0]) children();
}
module motor_holes() {
    for(sx=[-1,1],sy=[-1,1],dx=[-MOUNT_FOOT_X,MOUNT_FOOT_X])
        hole_z([sx*WHEEL_X+dx,sy*(MOTOR_FACE_Y+MOUNT_FOOT_Y)],BASE_T);
}
module base_plate() {
    difference() {
        rounded_box(CHASSIS_L,CHASSIS_W,BASE_T,5,true);
        motor_holes();
        for(p=concat(STAND_POINTS,BATTERY_POINTS)) hole_z(p,BASE_T);
        for(p=TOF_POINTS) hole_z([TOF_POS[0]+p[0],p[1]],BASE_T);
        for(p=BUMPER_POINTS) hole_z([BUMPER_POS[0]+p[0],p[1]],BASE_T);
        for(x=[-20,0,20],y=[-30,30]) hole_z([x,y],BASE_T);
        for(x=[-20,0,20]) translate([x,0,BASE_T/2])
            cube([8,24,BASE_T+2*EPS],center=true);
        for(x=[-20,20],y=[-17,17]) translate([x,y,BASE_T/2])
            cube([8,4.4,BASE_T+2*EPS],center=true);
    }
}
// Open-top rectangular saddle. Lower motor vertically, retain with TWO
// cable ties through transverse channels. Real torque/preload is unverified.
module n20_motor_mount() {
    total_l=N20_BODY_L+N20_GEARBOX_L;
    cavity_w=max(N20_BODY_W,N20_GEARBOX_W)+2*MOTOR_SIDE_CLEARANCE;
    difference() {
        union() {
            translate([-MOUNT_W/2,-total_l-1,0])
                rounded_box(MOUNT_W,total_l+2.5,MOUNT_T,1,false);
            translate([-(cavity_w+6)/2,-total_l-1,0])
                cube([cavity_w+6,total_l+1,MOUNT_TOP]);
            translate([-(cavity_w+6)/2,0,0])
                cube([cavity_w+6,1.5,MOUNT_AXIS_Z-3]);
        }
        translate([-(N20_BODY_W+2*MOTOR_SIDE_CLEARANCE)/2,
                   -total_l-EPS,MOUNT_AXIS_Z-N20_BODY_H/2])
            cube([N20_BODY_W+2*MOTOR_SIDE_CLEARANCE,N20_BODY_L+EPS,MOUNT_TOP+EPS]);
        translate([-(N20_GEARBOX_W+2*MOTOR_SIDE_CLEARANCE)/2,
                   -N20_GEARBOX_L-EPS,MOUNT_AXIS_Z-N20_GEARBOX_H/2])
            cube([N20_GEARBOX_W+2*MOTOR_SIDE_CLEARANCE,N20_GEARBOX_L+2*EPS,MOUNT_TOP+EPS]);
        for(x=[-MOUNT_FOOT_X,MOUNT_FOOT_X]) {
            hole_z([x,MOUNT_FOOT_Y],MOUNT_TOP);
            translate([x,MOUNT_FOOT_Y,MOUNT_T]) cylinder(d=M3_HEAD_D,h=MOUNT_TOP);
        }
        for(y=[-N20_GEARBOX_L-N20_BODY_L*0.3,-N20_GEARBOX_L-N20_BODY_L*0.75])
            translate([0,y,2]) cube([MOUNT_W+2*EPS,2.6,2],center=true);
    }
}
// Assembly-only rectangular envelope: NEVER print as hardware.
module n20_motor_placeholder(outward=1) {
    if(outward==-1) mirror([0,1,0]) motor_envelope(); else motor_envelope();
}
module motor_envelope() {
    translate([-N20_BODY_W/2,-N20_BODY_L-N20_GEARBOX_L,MOUNT_AXIS_Z-N20_BODY_H/2])
        cube([N20_BODY_W,N20_BODY_L,N20_BODY_H]);
    translate([-N20_GEARBOX_W/2,-N20_GEARBOX_L,MOUNT_AXIS_Z-N20_GEARBOX_H/2])
        cube([N20_GEARBOX_W,N20_GEARBOX_L,N20_GEARBOX_H]);
    translate([0,0,MOUNT_AXIS_Z]) rotate([-90,0,0]) cylinder(d=N20_SHAFT_D,h=N20_SHAFT_L);
}
// Printed disk prototype, matching hub pocket and bolt holes.
// Radial driver window must align with adapter set screw.
module wheel() {
    difference() {
        cylinder(d=WHEEL_D,h=WHEEL_W);
        translate([0,0,-EPS]) cylinder(d=HUB_FLANGE_D+HUB_POCKET_CLEARANCE,h=HUB_FLANGE_H+EPS);
        translate([0,0,-EPS]) cylinder(d=WHEEL_HUB_D+HUB_POCKET_CLEARANCE,h=HUB_H+0.2+EPS);
        translate([0,0,-EPS]) cylinder(d=WHEEL_BORE,h=WHEEL_W+2*EPS);
        for(a=HUB_BOLT_ANGLES) hole_z([HUB_BOLT_R*cos(a),HUB_BOLT_R*sin(a)],WHEEL_W);
        for(a=[0:30:330]) rotate([0,0,a])
            translate([WHEEL_D/2-1.5,0,WHEEL_W/2]) cube([3,3,WHEEL_W+2*EPS],center=true);
        rotate([0,0,HUB_SET_ANGLE]) translate([0,0,4.5])
            rotate([0,90,0]) cylinder(d=4.4,h=WHEEL_D/2+EPS);
    }
}
// Pocket faces up for printing; full outboard disk gives continuous bed contact.
module wheel_print() { translate([0,0,WHEEL_W]) rotate([180,0,0]) wheel(); }
module wheel_hub_adapter() {
    difference() {
        union() {
            cylinder(d=HUB_FLANGE_D,h=HUB_FLANGE_H);
            cylinder(d=WHEEL_HUB_D,h=HUB_H);
        }
        translate([0,0,-EPS]) cylinder(d=N20_SHAFT_D+0.25,h=HUB_H+2*EPS);
        for(a=HUB_BOLT_ANGLES) {
            p=[HUB_BOLT_R*cos(a),HUB_BOLT_R*sin(a)];
            hole_z(p,HUB_H);
            translate([p[0],p[1],-EPS]) hex_nut(M3_NUT_H+EPS);
        }
        rotate([0,0,HUB_SET_ANGLE]) {
            translate([0,0,4.5]) rotate([0,90,0]) cylinder(d=M3,h=HUB_FLANGE_D/2+EPS);
            // Nut loads down top slot; installed wheel retains it.
            translate([8,0,4.5]) rotate([0,90,0]) rotate([0,0,30]) hex_nut();
            translate([8,-M3_NUT_AF/sqrt(3),4.5]) cube([M3_NUT_H,2*M3_NUT_AF/sqrt(3),HUB_FLANGE_H]);
        }
    }
}
module battery_tray() {
    difference() {
        union() {
            rounded_box(BATTERY_L+10,BATTERY_W+10,BATTERY_RIM_H,4,true);
            for(p=BATTERY_POINTS) translate([p[0],p[1],0]) cylinder(d=10,h=BATTERY_FLOOR);
        }
        translate([-BATTERY_L/2,-BATTERY_W/2,BATTERY_FLOOR])
            cube([BATTERY_L,BATTERY_W,BATTERY_RIM_H+EPS]);
        for(p=BATTERY_POINTS) hole_z(p,BATTERY_RIM_H);
        for(x=[-20,20],y=[-17,17]) translate([x,y,BATTERY_RIM_H/2])
            cube([8,4.4,BATTERY_RIM_H+2*EPS],center=true);
    }
}
// Generic carrier: holes attach carrier to deck, NOT selected ESP32 PCB.
module esp32_tray() {
    difference() {
        rounded_box(58,32,3,4,true);
        for(p=ESP_POINTS) hole_z(p,3);
        for(y=[-12,12]) translate([0,y,1.5]) cube([18,2.6,3+2*EPS],center=true);
    }
}
// Forward upright carrier; lens aperture/tie slots are generic.
module camera_mount() {
    difference() {
        union() {
            rounded_box(24,36,3,2,true);
            translate([-12,-18,0]) cube([3,36,26]);
            for(y=[-2,5]) translate([-9,y,3]) rotate([90,0,0])
                linear_extrude(height=3) polygon([[0,0],[7,0],[0,7]]);
        }
        for(p=CAMERA_POINTS) hole_z(p,3);
        translate([-13,-10,10]) cube([5,20,12]);
        for(y=[-14,14]) translate([-13,y-1.3,9]) cube([5,2.6,14]);
    }
}
module camera_front_mount() { camera_mount(); }
// Upright face on bed avoids a long bridge over the lens opening.
module camera_mount_print() { translate([0,0,12]) rotate([0,-90,0]) camera_mount(); }
module tof_sensor_bar() {
    difference() {
        union() {
            translate([-2,-45,4]) rounded_box(4,90,26,2,false);
            for(y=[-12,12]) translate([-2,y-5,0]) cube([17,10,4]);
        }
        // Aperture lower edge is 2 mm above bumper; real sensor FOV unverified.
        for(y=[-32,0,32]) translate([-3,y,22]) rotate([0,90,0]) cylinder(d=8,h=6);
        for(p=TOF_POINTS) hole_z(p,4);
        for(y=[-32,0,32],dy=[-7.2,7.2])
            translate([-3,y+dy-1.3,16]) cube([6,2.6,12]);
    }
}
module top_deck() {
    difference() {
        rounded_box(DECK_L,DECK_W,DECK_T,5,true);
        for(p=STAND_POINTS) hole_z(p,DECK_T);
        for(p=ESP_POINTS) hole_z([ESP_POS[0]+p[0],p[1]],DECK_T);
        for(p=CAMERA_POINTS) hole_z([CAMERA_POS[0]+p[0],p[1]],DECK_T);
        translate([-28,0,DECK_T/2]) cube([14,24,DECK_T+2*EPS],center=true);
    }
}
// Back face on bed avoids supporting the elevated sensor beam.
module tof_sensor_bar_print() { translate([0,0,2]) rotate([0,-90,0]) tof_sensor_bar(); }
module top_cover() { top_deck(); }
module standoff() { difference() { cylinder(d=STAND_D,h=STAND_H); hole_z([0,0],STAND_H); } }
// One export contains FOUR deliberately separate spacers.
module standoffs() { for(x=[-8,8],y=[-8,8]) translate([x,y,0]) standoff(); }
module front_bumper() {
    difference() {
        union() {
            translate([-2,-55,0]) rounded_box(4,110,16,2,false);
            translate([0,-6,0]) cube([28,12,3]);
        }
        for(p=BUMPER_POINTS) hole_z(p,3);
    }
}
module fit_coupon() {
    difference() {
        rounded_box(60,20,5,2,true);
        for(i=[0:3]) translate([-22+12*i,0,-EPS]) cylinder(d=3.1+0.1*i,h=5+2*EPS);
        translate([24,0,-EPS]) cylinder(d=N20_SHAFT_D+0.25,h=5+2*EPS);
    }
}
// Indexed component exports allow actual independent-solid interference checks.
// 0 base; 1..4 mounts; 5..8 motor envelopes; 9..12 wheels; 13..16 hubs;
// 17 battery; 18 deck; 19..22 spacers; 23 ESP; 24 camera; 25 ToF; 26 bumper.
module assembly_component(i) {
    sx=(i-1)%2==0?-1:1;
    sy=floor((i-1)%4/2)==0?-1:1;
    if(i==0) base_plate();
    else if(i>=1 && i<=4) side_placement(sx,sy) n20_motor_mount();
    else if(i>=5 && i<=8) side_placement(sx,sy) motor_envelope();
    else if(i>=9 && i<=12) axle_placement(sx,sy) wheel();
    else if(i>=13 && i<=16) axle_placement(sx,sy) wheel_hub_adapter();
    else if(i==17) translate([0,0,BASE_T]) battery_tray();
    else if(i==18) translate([0,0,DECK_Z]) top_deck();
    else if(i>=19 && i<=22) translate([STAND_POINTS[i-19][0],STAND_POINTS[i-19][1],BASE_T]) standoff();
    else if(i==23) translate([ESP_POS[0],ESP_POS[1],DECK_Z+DECK_T]) esp32_tray();
    else if(i==24) translate([CAMERA_POS[0],CAMERA_POS[1],DECK_Z+DECK_T]) camera_mount();
    else if(i==25) translate([TOF_POS[0],TOF_POS[1],BASE_T]) tof_sensor_bar();
    else if(i==26) translate([BUMPER_POS[0],BUMPER_POS[1],BASE_T]) front_bumper();
}
module assembly(show_motors=true,show_wheels=true,show_deck=true) {
    for(i=[0:26]) if((show_motors || i<5 || i>8) && (show_wheels || i<9 || i>16) && (show_deck || i<18 || i>24))
        color(i>=5 && i<=8?"silver":i>=9 && i<=16?"#303030":i==17 || i>=23 && i<=25?"orange":"gold")
            assembly_component(i);
}
assembly();

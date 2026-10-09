
$fn=96;
use <mechanical_source_snapshot.scad>;
module actual_nut() { cylinder(r=5.5/sqrt(3),h=2.4,$fn=6); }
module heads_and_tools(points,foot_h) {
    for(p=points) {
        translate([p[0],p[1],foot_h]) cylinder(d=6.6,h=3);
        translate([p[0],p[1],foot_h+3]) cylinder(d=8,h=30);
    }
}
module axial_hardware() {
    for(a=[90,210,330]) {
        p=[9*cos(a),9*sin(a)];
        translate([p[0],p[1],0.1]) actual_nut();
        translate([p[0],p[1],0]) cylinder(d=3,h=14);
        translate([p[0],p[1],14]) cylinder(d=6.6,h=3);
    }
}
module radial_hardware(a=30,tool=true) {
    rotate([0,0,a]) {
        translate([8.1,0,4.5]) rotate([0,90,0]) rotate([0,0,30]) actual_nut();
        translate([1.6,0,4.5]) rotate([0,90,0]) cylinder(d=3,h=10);
        if(tool) translate([11.6,0,4.5]) rotate([0,90,0]) cylinder(d=3,h=20);
    }
}
module placed_hub_shanks(length=14) {
    for(sx=[-1,1],sy=[-1,1]) axle_placement(sx,sy)
        for(a=[90,210,330])
            translate([9*cos(a),9*sin(a),14-length]) cylinder(d=3,h=length);
}
intersection() {
        union() for(i=[1:4]) assembly_component(i);
        placed_hub_shanks(16);
    }

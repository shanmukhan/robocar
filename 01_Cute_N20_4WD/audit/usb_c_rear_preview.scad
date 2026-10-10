// View-only rear USB-C integration: green box is the reserved module envelope.
// The actual electronics/USB receptacle remain subject to purchased fit checks.
$fn=96;
use <../cute_rover_complete.scad>;
assembly();
color("#33945f") translate([39,32.5,41]) charger_board_envelope();

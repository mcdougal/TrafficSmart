var c = document.getElementById("canvas");
var context = c.getContext("2d");

var NORTH = "north";
var SOUTH = "south";
var EAST = "east";
var WEST = "west";

function clear() {
    context.clearRect(0, 0, c.width, c.height);
}
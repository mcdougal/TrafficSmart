// streets
var blockLineWidth = 1;
var lightLength = blockSize / 4;
var lightLineWidth = 8;
var streetLengthInCars = 6;
var blockLineColor = '#000';
var redLightColor = '#f00';
var greenLightColor = '#0f0';
var lightFocusedColor = '#00f';

// cars
var carLength = blockSize / streetLengthInCars;
var carHeadLength = carLength * .25;
var carBodyLength = carLength * .5;
var carWidth = carLength * .75;
var carBodyWidth = carWidth * .75;
var carHeadWidth = carWidth * .75;
var carBlinkerWidth = carHeadWidth / 2;
var streetBuffer = 10;
var lightBuffer = 10;
var carColor = '#000';
var carFocusedColor = '#00f';
var carMovedColor = '#ccc';
var carBlockedColor = '#99f';
var blinkerOnColor = '#ff0';
var blinkerOffColor = '#ccc';

function drawBlock(cx,cy) {
    context.beginPath();
    context.lineWidth = blockLineWidth;
    context.strokeStyle = blockLineColor;
    context.moveTo(cx-lightLength, cy);
    context.lineTo(cx-(blockSize-lightLength), cy);
    context.moveTo(cx+lightLength, cy);
    context.lineTo(cx+(blockSize-lightLength), cy);
    context.moveTo(cx, cy-lightLength);
    context.lineTo(cx, cy-(blockSize-lightLength));
    context.moveTo(cx, cy+lightLength);
    context.lineTo(cx, cy+(blockSize-lightLength));
    context.stroke();
    context.closePath();
}

function drawLight(x1,y1,x2,y2,color,focused,width) {
    context.beginPath();
    if (width !== null) {
	context.lineWidth = width;
    }
    else {	
	context.lineWidth = lightLineWidth;
    }
    if (focused) {
	context.strokeStyle = lightFocusedColor;
    }
    else {
	context.strokeStyle = color;
    }
    context.moveTo(x1,y1);
    context.lineTo(x2,y2);
    context.stroke();
    context.closePath();
}

function drawHorizontalLight(cx,cy,color,focused,width) {
    drawLight(cx-lightLength,cy,cx+lightLength,cy,color,focused,width);
}

function drawVerticalLight(cx,cy,color,focused,width) {
    drawLight(cx,cy-lightLength,cx,cy+lightLength,color,focused,width);
}

function drawIntersection(x,y,green,focused) {
    var x = blockSize*x;
    var y = blockSize*y;
    var cx = x + blockSize;
    var cy = y + blockSize;

    drawBlock(cx,cy);

    if (green == "h") {
        drawVerticalLight(cx,cy,blockLineColor,false,blockLineWidth);
        drawHorizontalLight(cx,cy,greenLightColor,focused,null);
    }
    else {
        drawHorizontalLight(cx,cy,blockLineColor,false,blockLineWidth);
        drawVerticalLight(cx,cy,greenLightColor,focused,null);
    }
}

function drawCar(ix, iy, dir, pos, turning, focused, moved, blocked) {
    var ix = blockSize*ix;
    var iy = blockSize*iy;
    var icx = ix + blockSize;
    var icy = iy + blockSize;
    var lengthAdjust = (carLength - (carHeadLength+carBodyLength)) / 2;
    var widthAdjust = ((carWidth - carBodyWidth) / 2);

    if (dir == NORTH) {
        var cx = icx - carWidth + widthAdjust - streetBuffer;
        var cy = icy - ((carLength+streetBuffer)*(pos+1)) + lengthAdjust;
        var bodyX = cx;
        var bodyY = cy;
	var bodyLength = carBodyWidth;
	var bodyHeight = carBodyLength;
	var blinkerRightX = cx;
	var blinkerRightY = cy + bodyHeight;
	var blinkerRightLength = carBlinkerWidth;
	var blinkerRightHeight = carHeadLength;
	var blinkerLeftX = cx + carBlinkerWidth;
	var blinkerLeftY = cy + bodyHeight;
	var blinkerLeftLength = carBlinkerWidth;
	var blinkerLeftHeight = carHeadLength;
    }
    else if (dir == SOUTH) {
        var cx = icx + widthAdjust + streetBuffer;
        var cy = icy + ((carLength+streetBuffer)*pos) + lengthAdjust + streetBuffer;
	var blinkerRightX = cx + carBlinkerWidth;
	var blinkerRightY = cy;
	var blinkerRightLength = carBlinkerWidth;
	var blinkerRightHeight = carHeadLength;
	var blinkerLeftX = cx;
	var blinkerLeftY = cy;
	var blinkerLeftLength = carBlinkerWidth;
	var blinkerLeftHeight = carHeadLength;
        var bodyX = cx;
        var bodyY = cy + carHeadLength;
	var bodyLength = carBodyWidth;
	var bodyHeight = carBodyLength;
    }
    else if (dir == EAST) {
        var cx = icx + ((carLength+streetBuffer)*pos) + lengthAdjust + streetBuffer;
        var cy = icy - carWidth + widthAdjust - streetBuffer;
	var blinkerRightX = cx;
	var blinkerRightY = cy;
	var blinkerRightLength = carHeadLength;
	var blinkerRightHeight = carBlinkerWidth;
	var blinkerLeftX = cx;
	var blinkerLeftY = cy + carBlinkerWidth;
	var blinkerLeftLength = carHeadLength;
	var blinkerLeftHeight = carBlinkerWidth;
        var bodyX = cx + carHeadLength;
        var bodyY = cy;
	var bodyLength = carBodyLength;
	var bodyHeight = carBodyWidth;
    }
    else if (dir == WEST) {
        var cx = icx - ((carLength+streetBuffer)*(pos+1)) + lengthAdjust;
        var cy = icy + widthAdjust + streetBuffer;
        var bodyX = cx;
        var bodyY = cy;
	var bodyLength = carBodyLength;
	var bodyHeight = carBodyWidth;
	var blinkerRightX = cx + bodyLength;
	var blinkerRightY = cy + carBlinkerWidth;
	var blinkerRightLength = carHeadLength;
	var blinkerRightHeight = carBlinkerWidth;
	var blinkerLeftX = cx + bodyLength;
	var blinkerLeftY = cy;
	var blinkerLeftLength = carHeadLength;
	var blinkerLeftHeight = carBlinkerWidth;
    }

    if (turning == "right") {
	var blinkerRightColor = blinkerOnColor;
    }
    else {
	var blinkerRightColor = blinkerOffColor;
    }
    if (turning == "left") {
	var blinkerLeftColor = blinkerOnColor;
    }
    else {
	var blinkerLeftColor = blinkerOffColor;
    }

    context.lineWidth = 1;

    if (focused) {
	context.fillStyle = carFocusedColor;
    }
    else if (moved) {
	context.fillStyle = carMovedColor;
    }
    else if (blocked) {
	context.fillStyle = carBlockedColor;
    }
    else {
	context.fillStyle = carColor;
    }
    context.fillRect(bodyX,bodyY,bodyLength,bodyHeight);

    context.fillStyle = blinkerRightColor;
    context.fillRect(
	blinkerRightX,
	blinkerRightY,
	blinkerRightLength,
	blinkerRightHeight);

    context.fillStyle = blinkerLeftColor;
    context.fillRect(
	blinkerLeftX,
	blinkerLeftY,
	blinkerLeftLength,
	blinkerLeftHeight);
}
var PLAY_ICON = new Image();
var PAUSE_ICON = new Image();
PLAY_ICON.src = 'http://www.finkworld.co.uk/wp-content/uploads/playButton.png'
PAUSE_ICON.src = 'http://www.olotolo.com/sciencegames/Photos/PauseButton.png'

var isPlaying = false;
var playTimeout = null;
var playIconVisible = false;
var pauseIconVisible = false;
var navIconTimeout = null;
var previousFrame = null;
var thisFrame = null;
var nextFrame = null;
var lastFrame = null;

function drawNavIcon() {
    if (playIconVisible) {
        context.drawImage(PLAY_ICON, 5, 5);
    }
    if (pauseIconVisible) {
        context.drawImage(PAUSE_ICON, 5, 5);
    }
}

function drawCycle(step) {
    context.fillStyle = "#000";
    context.font = "50px Arial";
    context.textAlign = "right";
    context.fillText(step, 670, 45);
}

function drawSubCycle(step) {
    context.fillStyle = "#666";
    context.font = "23px Arial";
    context.textAlign = "right";
    context.fillText(step, 665, 78);
}

function drawFrame(step) {
    context.fillStyle = "#666";
    context.font = "23px Arial";
    context.textAlign = "right";
    context.fillText(step, 665, 109);
}

function drawMessage(msg) {
    context.fillStyle = "#000";
    context.font = "14px Arial";
    context.textAlign = "left";
    context.fillText(msg, 10, 590);
}

function drawSpeed() {
    context.fillStyle = "#666";
    context.font = "24px Arial";
    context.textAlign = "right";
    context.fillText(speed, 665, 590);
}

function play() {
    if (isPlaying) {
	return
    }
    isPlaying = true;
    showNavIcon(true, false);
}

function pause() {
    if (playTimeout !== null) {
	clearTimeout(playTimeout);
    }
    isPlaying = false;
    showNavIcon(false, true);
}

function showNavIcon(playIcon, pauseIcon) {
    playIconVisible = playIcon;
    pauseIconVisible = pauseIcon;
    if (navIconTimeout !== null) {
	clearTimeout(navIconTimeout);
    }
    navIconTimeout = setTimeout(function() {
	playIconVisible = false;
	pauseIconVisible = false;
    }, 2000);
}

function drawNextFrame() {
    if (isPlaying) {
	playTimeout = setTimeout(nextFrame, speed);
    }
}

var gotoFrame = null;
document.onkeydown = function(e) {
    e = e || window.event;
    var frame = null;

    // alert(e.keyCode);

    // o
    if (e.keyCode == '79') {
	frame = previousFrame;
    }
    // p
    if (e.keyCode == '80') {
	frame = nextFrame;
    }

    // left
    if (e.keyCode == '37') {
	frame = previousTimestep;
    }
    // right
    if (e.keyCode == '39') {
	frame = nextTimestep;
    }

    // k
    if (e.keyCode == '75') {
	frame = previousCycle;
    }
    // l
    if (e.keyCode == '76') {
	frame = nextCycle;
    }

    // n
    if (e.keyCode == '78') {
	frame = frame0;
    }
    // m
    if (e.keyCode == '77') {
	frame = lastFrame;
    }

    // abort playing on certain keypresses
    if (frame !== null) {
	if (isPlaying) {
	    pause();
	}
	frame();
    }

    // [
    if (e.keyCode == '219') {
	if (speed >= 10) {
	    speed -= 10;
	}
	thisFrame();
    }
    // ]
    if (e.keyCode == '221') {
	speed += 10;
	thisFrame();
    }

    // j
    if (e.keyCode == '74') {
	gotoFrame = "";
	thisFrame();
	$('#frame-select-box').show();
	$('#frame-select-txt').show();
    }
    // 0-9
    var nums = ['48','49','50','51','52','53','54','55','56','57'];
    var keynum = nums.indexOf(""+e.keyCode);
    if (keynum != -1) {
	if (gotoFrame !== null) {
	    gotoFrame += ""+keynum;
	    func = window["frame"+gotoFrame];
	    if (typeof func == 'function') {
		func();
	    }
	}
    }
    // enter
    if (e.keyCode == '13') {
	gotoFrame = null;
	thisFrame();
	$('#frame-select-box').hide();
	$('#frame-select-txt').hide();
    }

    // spacebar
    if (e.keyCode == '32') {
	if (isPlaying) {
            pause();
	}
	else {
            play();
	}
	thisFrame();
    }
}

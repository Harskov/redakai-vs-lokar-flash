// resets the score counters and the lives, then attaches the game's sounds from the library:
// intro starts at once and loops, pb and cra each get an empty clip of their own
stop();
var scorecard = 0;
var scorecard2 = 0;
var levelscore = 0;
var lifee = 5;
var intro = new Sound();
intro.attachSound("bat_sound");
_root.intro.start(0, 9999);
var accSnd = new Sound();
accSnd.attachSound("accSnd");
var accLoop = new Sound();
accLoop.attachSound("accLoop");
var pb = new Sound(_root.createEmptyMovieClip("play bg2", 7010));
pb.attachSound("play bg1");
var cra = new Sound(_root.createEmptyMovieClip("crashbike1", 9010));
cra.attachSound("crashbike");

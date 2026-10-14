// @reference DoInitAction_main
// @reference updateSoundLoop
// @reference soundOff
// @reference soundOn
// @reference gameStart
// @reference nextLevel
// restart the current level: reset the stargeted count, then step the timeline
// through "reset" back to "game" (nextLevel does the same after level++)
function replay()
{
   stargeted = 0.0;
   this.gotoAndStop("reset");
   this.gotoAndStop("game");
}
// @reference newGame
// @reference playSnd
// @reference initLevel
// @reference processGame
// @reference fire
// @reference resetkfire
// the clock readout: the elapsed game time (timeCounter) formatted into txtTime
function showTime()
{
   txtTime = getTimeString(timeCounter);
}
// @reference getTimeString
// @reference resume
// @reference pauseGame
// @reference clearStuff
// @reference loose
// @reference calcBikeNVector

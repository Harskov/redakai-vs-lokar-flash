// @reference DoInitAction_main
// @reference updateSoundLoop
// @reference soundOff
// @reference soundOn
// @reference gameStart
// @reference nextLevel
// the replay option: clear the flag, then step the timeline through "reset" back to "game"
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
// the clock readout: format the remaining/elapsed time into the text field
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

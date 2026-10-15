// @reference DoInitAction_main
// @reference updateSoundLoop
// mutes the music: the loop clip in use (mc_sloop_zast while zastSoundFlag is set, else mc_sloop) goes to frame 3
function soundOff()
{
   if(zastSoundFlag)
   {
      mc_sloop_zast.gotoAndStop(3);
   }
   else
   {
      mc_sloop.gotoAndStop(3);
   }
   stopSoundFlag = true;
}
// unmutes the music: the loop clip in use goes back to frame 2
function soundOn()
{
   if(zastSoundFlag)
   {
      mc_sloop_zast.gotoAndStop(2);
   }
   else
   {
      mc_sloop.gotoAndStop(2);
   }
   stopSoundFlag = false;
}
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

// the game's init script, run once: its functions, then its variables with their starting values
function updateSoundLoop()
{ /* @reference updateSoundLoop */ }
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
// a new game: zero scores, timeCounter and stargeted, ten lives, the music over to mc_sloop
// (updateSoundLoop with zastSoundFlag cleared, unless muted), then level 0 so that
// nextLevel steps into level 1
function gameStart()
{
   scores = 0;
   timeCounter = 0;
   stargeted = 0;
   life = 10;
   zastSoundFlag = false;
   updateSoundLoop();
   level = 0;
   nextLevel();
}
// after level 10 the game starts over (newGame); otherwise the next level, stepping
// the timeline through "reset" back to "game" as replay does
function nextLevel()
{
   stargeted = 0;
   levelTimeCounter = 0;
   if(level == 10)
   {
      newGame();
      return;
   }
   level++;
   this.gotoAndStop("reset");
   this.gotoAndStop("game");
}
// restart the current level: reset the stargeted count, then step the timeline
// through "reset" back to "game" (nextLevel does the same after level++)
function replay()
{
   stargeted = 0;
   this.gotoAndStop("reset");
   this.gotoAndStop("game");
}
function newGame()
{ /* @reference newGame */ }
// plays a library sound by its linkage name: attach it to a Sound on this timeline and start it
function playSnd(lib_snd)
{
   s = new Sound(this);
   s.attachSound(lib_snd);
   s.start();
}
function initLevel()
{ /* @reference initLevel */ }
function processGame()
{ /* @reference processGame */ }
// plays the newest shot (bullet_id<kval>, which processGame attached 50 ms earlier) from frame 2
function fire()
{
   eval("_root.bullet_id" + kval).gotoAndPlay(2);
}
// re-arms the gun: processGame clears kfire when it fires a shot and calls this 290 ms later
function resetkfire()
{
   kfire = true;
}
// the clock readout: the elapsed game time (timeCounter) formatted into txtTime
function showTime()
{
   txtTime = getTimeString(timeCounter);
}
function getTimeString(time)
{ /* @reference getTimeString */ }
// undo pauseGame: clear the message box ("empty"), restart the rider's animation, gameState 0;
// mc_sloop (probably the looping sound's clip) goes back to frame 2 unless sound is off
function resume()
{
   // !FAKE: the author wrote if(!stopSoundFlag); the doubled parentheses keep the double Not before the branch
   if((!stopSoundFlag))
   {
      mc_sloop.gotoAndStop(2);
   }
   mc_messageF.gotoAndStop(1);
   mc_messageF.mc_message.gotoAndStop("empty");
   bikeSync.mc_bike.mc.mc_body_man.mc.startAnim();
   gameState = 0;
}
// pause the game: show the "pause" message, stop the rider's animation, gameState 4;
// mc_sloop (probably the looping sound's clip) goes to frame 3 unless sound is off
function pauseGame()
{
   // !FAKE: the author wrote if(!stopSoundFlag); the doubled parentheses keep the double Not before the branch
   if((!stopSoundFlag))
   {
      mc_sloop.gotoAndStop(3);
   }
   mc_messageF.mc_message.gotoAndStop("pause");
   bikeSync.mc_bike.mc.mc_body_man.mc.stopAnim();
   gameState = 4;
}
function clearStuff()
{ /* @reference clearStuff */ }
// a lost life (the author's "loose" for lose): fail sound, one life off, the wheels moved
// 1000 px right (probably off the stage), the crash clips played, the times and score shown
function loose()
{
   clearStuff();
   _root.txtscore.text = _root.tscore;
   _root.mscore = _root.tscore;
   // !FAKE: the author wrote if(!stopSoundFlag); the doubled parentheses keep the double Not before the branch
   if((!stopSoundFlag))
   {
      mc_sloop.gotoAndStop(3);
   }
   // !FAKE: the author wrote if(!stopSoundFlag); the doubled parentheses keep the double Not before the branch
   if((!stopSoundFlag))
   {
      playSnd("lib_snd_fail");
   }
   mc_messageF.gotoAndPlay(2);
   _root.life--;
   bikeSync.mc_back_wheel._x += 1000;
   bikeSync.mc_forward_wheel._x += 1000;
   _root.bikeSync.mc_bike.mc.jeep.car1.gotoAndPlay(2);
   _root.bikeSync.mc_bike.mc.jeep.car2.gotoAndPlay(2);
   _root.bikeSync.mc_bike.mc.jeep.car3.gotoAndPlay(2);
   _root.crash.gotoAndPlay(2);
   _root.scores = 0;
   mc_messageF.mc_message.levelTime = getTimeString(levelTimeCounter);
   mc_messageF.mc_message.commonTime = getTimeString(timeCounter);
   mc_messageF.mc_message.scores = scores;
   bikeSync.mc_bike.mc.mc_body_man.mc.stopAnim();
   bikeSync.mc_bike.mc.mc_body_man.mc.stopMCAnim();
   gameState = 1;
}
function calcBikeNVector()
{ /* @reference calcBikeNVector */ }
var lastTimer;
var level;
var stopSoundFlag = false;
var bikeSync = null;
var engine = null;
var objCamera = null;
var back1 = null;
var back2 = null;
var gameState;
var zastSoundFlag = true;
var accFlag;
var accCounter;
var timeCounter;
var levelTimeCounter;
var scores;
var highQuality = true;
var life = 10;
var stargeted;

// the game's init script, run once: its functions, then its variables with their starting values
function updateSoundLoop()
{ /* @reference updateSoundLoop */ }
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
function replay()
{
   stargeted = 0;
   this.gotoAndStop("reset");
   this.gotoAndStop("game");
}
function newGame()
{ /* @reference newGame */ }
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
function fire()
{
   eval("_root.bullet_id" + kval).gotoAndPlay(2);
}
function resetkfire()
{
   kfire = true;
}
function showTime()
{
   txtTime = getTimeString(timeCounter);
}
function getTimeString(time)
{ /* @reference getTimeString */ }
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

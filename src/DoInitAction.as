// the game's init script, run once: its functions, then its variables with their starting values
// keeps the music loop in step with the mute state: with the sound on, the loop in use
// (mc_sloop_zast while zastSoundFlag is set, else mc_sloop) plays at frame 2 and the other sits at 3
function updateSoundLoop()
{
   // !FAKE: the author wrote if(!stopSoundFlag); the doubled parentheses keep the double Not before the branch
   if((!stopSoundFlag))
   {
      if(zastSoundFlag)
      {
         mc_sloop.gotoAndStop(3);
         mc_sloop_zast.gotoAndStop(2);
      }
      else
      {
         mc_sloop.gotoAndStop(2);
         mc_sloop_zast.gotoAndStop(3);
      }
   }
}
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
// a new game starts on the `main` frame, with stargeted cleared and the zast sound switched back on
function newGame()
{
   stargeted = 0;
   zastSoundFlag = true;
   updateSoundLoop();
   this.gotoAndStop("main");
}
// plays a library sound by its linkage name: attach it to a Sound on this timeline and start it
function playSnd(lib_snd)
{
   s = new Sound(this);
   s.attachSound(lib_snd);
   s.start();
}
// sets up level `level`: the minimap's marks, the level clip, the bike's three particles and its springs, the camera, the sound loop
// registers: r1 = the counter (i), r2 = the particle at the forward wheel (forwardPart), r3 = the particle at the bike (bikePart), r4 = the particle at the back wheel (backPart)
function initLevel()
{
   lastTimer = getTimer();
   mc_level.mc_minimap._visible = true;
   mc_level.mc_minimap.mc_stage.gotoAndStop(level);
   if(level > 1)
   {
      var i = 1;
      while(i < level)
      {
         mc_level.mc_minimap["s" + i].gotoAndStop(2);
         i++;
      }
   }
   mc_level.mc_minimap["s" + level].gotoAndStop(3);
   mc_level.gotoAndStop(level);
   mc_level.mc.mc_hit._visible = false;
   if(bikeSync == null)
   {
      bikeSync = new CBikeSynchronizer();
      engine = new CParticleEngine();
      objCamera = new CCamera();
      back1 = new CBack();
      back2 = new CBack();
   }
   else
   {
      engine.clear();
   }
   back1.init(mc_level.mc.mc_fon.mc_grass.mc1, mc_level.mc.mc_fon.mc_grass.mc2, 1);
   back2.init(mc_level.mc.mc_fon.mc_hill.mc1, mc_level.mc.mc_fon.mc_hill.mc2, 2);
   bikeSync.init(mc_level.mc.mc_bike, 0, 0);
   var backPart = new CParticle(bikeSync.mc_back_wheel._x, bikeSync.mc_back_wheel._y, 3);
   engine.addParticle(backPart);
   engine.addWheel(bikeSync.mc_back_wheel, backPart, 28.5, 17.5);
   var forwardPart = new CParticle(bikeSync.mc_forward_wheel._x, bikeSync.mc_forward_wheel._y, 3);
   engine.addParticle(forwardPart);
   engine.addWheel(bikeSync.mc_forward_wheel, forwardPart, 10.5, 17.5);
   var bikePart = new CParticle(bikeSync.mc_bike._x, bikeSync.mc_bike._y, 3);
   bikePart.mc = mc_level.mc.mc_bike.mc_test;
   engine.addParticle(bikePart);
   engine.addSpringConstraint(backPart, forwardPart, 0.45, 0.5);
   engine.addSpringConstraint(backPart, bikePart, 0.45, 0.55);
   engine.addSpringConstraint(bikePart, forwardPart, 0.45, 0.7);
   bikeSync.setParticles(bikePart, backPart, forwardPart);
   objCamera.init(bikeSync.mc_bike, mc_level.mc);
   engine.setHitMovie(mc_level.mc.mc_hit);
   engine.start();
   accFlag = false;
   accCounter = 50;
   // !FAKE: the author wrote if(!stopSoundFlag); the doubled parentheses keep the double Not before the branch
   if((!stopSoundFlag))
   {
      mc_sloop.gotoAndStop(2);
   }
   mc_messageF.gotoAndStop(1);
   mc_messageF.mc_message.gotoAndStop("empty");
   gameState = 0;
   i = 1;
   while(i <= 10)
   {
      mc_level.mc["s" + i].gotoAndStop(Math.floor(Math.random() * 3 + 1));
      i++;
   }
}
// the game's per-frame step (the frame-15 clip's enterFrame calls it): while gameState is 0, the clock,
// the arrow-key tilt, the physics, the pickups, the shots (F, G), the finish and the rider's hit tests
// !FAKE: the author wrote _root; eval("_root") keeps the original DefineFunction, which reads _root by name
function processGame()
{
   engine.gravity = 4;
   var _loc7;
   var _loc6;
   _loc7 = getTimer();
   _loc6 = _loc7 - lastTimer;
   txtFps = 1 / (_loc6 / 1000);
   lastTimer = _loc7;
   if(gameState == 0)
   {
      timeCounter += _loc6;
      levelTimeCounter += _loc6;
      showTime();
      var _loc9 = 0;
      var _loc8 = 0;
      var _loc3;
      var _loc5;
      accCounter++;
      // !FAKE: the author wrote if(!accFlag); the doubled parentheses keep the double Not before the branch
      if((!accFlag))
      {
         // key 38 is the Up arrow
         accFlag = Key.isDown(38);
         if(accFlag && accCounter > 10)
         {
            accCounter = 0;
            // !FAKE: the author wrote if(!stopSoundFlag); the doubled parentheses keep the double Not before the branch
            if((!stopSoundFlag))
            {
               mc_gas.gotoAndPlay(2);
            }
         }
      }
      else
      {
         accFlag = Key.isDown(38);
      }
      if(Key.isDown(CMan.LEFT_BUTTON))
      {
         _loc3 = calcBikeNVector();
         if(_loc3.y > 0)
         {
            _loc5 = Math.abs(_loc3.y) * 0.2 + 0.8;
            bikeSync.mc_forward_wheel.addedAcc.x -= _loc3.x * engine.gravity / 1.1 * _loc5;
            bikeSync.mc_forward_wheel.addedAcc.y -= _loc3.y * engine.gravity * 1.3 * _loc5;
            bikeSync.mc_back_wheel.addedAcc.x += _loc3.x * engine.gravity / 1.5 * _loc5;
            bikeSync.mc_back_wheel.addedAcc.y += _loc3.y * engine.gravity * _loc5;
         }
      }
      else if(Key.isDown(CMan.RIGHT_BUTTON))
      {
         _loc3 = calcBikeNVector();
         if(_loc3.y > 0)
         {
            _loc5 = Math.abs(_loc3.y) * 0.2 + 0.8;
            bikeSync.mc_forward_wheel.addedAcc.x += _loc3.x * engine.gravity / 1.5 * _loc5;
            bikeSync.mc_forward_wheel.addedAcc.y += _loc3.y * engine.gravity * _loc5;
            bikeSync.mc_back_wheel.addedAcc.x -= _loc3.x * engine.gravity / 1.1 * _loc5;
            bikeSync.mc_back_wheel.addedAcc.y -= _loc3.y * engine.gravity * 1.3 * _loc5;
         }
      }
      engine.process();
      bikeSync.process();
      objCamera.process();
      back1.process(mc_level.mc._x);
      back2.process(mc_level.mc._x);
      mc_level.mc.mc_fon._x = -mc_level.mc._x;
      var _loc1 = 1;
      while(_loc1 <= 20)
      {
         if(mc_level.mc["s" + _loc1]._visible == true && bikeSync.mc_bike.hitTest(mc_level.mc["s" + _loc1]) && !mc_level.mc["s" + _loc1].bikehit)
         {
            mc_level.mc["s" + _loc1].bikehit = true;
            mc_level.mc["s" + _loc1].pio.gotoAndPlay(2);
         }
         _loc1++;
      }
      // stargeted is forced to 5 every frame, so the stargeted >= 3 tests below always pass
      // (probably a leftover that switched the target count off)
      stargeted = 5;
      if(bikeSync.mc_bike._x + mc_level.mc.mc_bike._x >= mc_level.mc.mc_finish._x - 190 && stargeted >= 3)
      {
         if(mc_level.mc.maskman_mc._currentframe == 1)
         {
            mc_level.mc.maskman_mc.gotoAndPlay(2);
            eval("_root").themask_mc.gotoAndStop(508);
         }
      }
      if(kfire == undefined)
      {
         kfire = true;
         eval("_root").bulletArray = new Array();
      }
      // keys 71 and 70 are G (a bullet) and F (a rocket)
      if(Key.isDown(71) && kfire == true || Key.isDown(70) && kfire == true)
      {
         if(Key.isDown(70))
         {
            weapontype = "rocket";
         }
         else
         {
            weapontype = "bullet";
         }
         eval("_root").kfire = false;
         var p_a = eval("_root").my2 - eval("_root").my1;
         var p_b = eval("_root").mx2 - eval("_root").mx1;
         var p_radians = Math.atan2(p_a, p_b);
         // 0.01745329 is pi / 180: radians to degrees
         var degrees = p_radians / 0.01745329;
         var angle = Math.round(degrees);
         if(kval == undefined)
         {
            kval = 1000;
         }
         else
         {
            kval++;
            if(kval > 1100)
            {
               kval = 1000;
            }
         }
         if(tcheck == undefined)
         {
            tcheck = 1;
         }
         else
         {
            tcheck++;
         }
         if(tcheck > 20)
         {
            delete tmparray;
            tmparray = new Array();
            var tlen = eval("_root").bulletArray.length;
            if(tlen > 0)
            {
               j = 0;
               while(j < tlen)
               {
                  if(eval("_root").bulletArray[j] != "")
                  {
                     tmparray.push(eval("_root").bulletArray[j]);
                  }
                  else
                  {
                     eval("_root").arrdeactivate = true;
                  }
                  j++;
               }
               eval("_root").bulletArray = tmparray;
               eval("_root").arrdeactivate = false;
            }
            tcheck = 1;
         }
         if(weapontype == "bullet")
         {
            eval("_root").attachMovie("bullet_id", "bullet_id" + kval, eval("_root").getNextHighestDepth());
            eval("_root.bullet_id" + kval)._rotation = angle;
            eval("_root.bullet_id" + kval).weapontype = weapontype;
            eval("_root.bullet_id" + kval)._x = eval("_root").mx3;
            eval("_root.bullet_id" + kval)._y = eval("_root").my3;
         }
         else
         {
            eval("_root").attachMovie("rocket_id", "bullet_id" + kval, eval("_root").getNextHighestDepth());
            eval("_root.bullet_id" + kval)._rotation = angle - 40;
            eval("_root.bullet_id" + kval).weapontype = weapontype;
            eval("_root.bullet_id" + kval)._x = eval("_root").mx3 - 40;
            eval("_root.bullet_id" + kval)._y = eval("_root").my3 - 30;
         }
         eval("_root").bulletArray.push("bullet_id" + kval);
         setTimeout(fire, 50);
         setTimeout(resetkfire, 290);
      }
      if(eval("_root").helicounter == undefined)
      {
         eval("_root").helicounter = 1;
      }
      eval("_root").helicounter += 1;
      if(eval("_root").helicounter == 200)
      {
         eval("_root").helicop._x = 786.4;
         eval("_root").heliactivate = true;
         eval("_root").helicop._rotation = 0;
         setTimeout(eval("_root").firebomb, 1800);
      }
      if(bikeSync.mc_bike._x + mc_level.mc.mc_bike._x >= mc_level.mc.mc_finish._x && stargeted >= 3)
      {
         // !FAKE: the author wrote if(!stopSoundFlag); the doubled parentheses keep the double Not before the branch
         if((!stopSoundFlag))
         {
            mc_sloop.gotoAndStop(3);
         }
         if(level <= 10)
         {
            clearStuff();
            gotoAndStop("comple");
            gameState = 2;
         }
         else
         {
            mc_messageF.mc_message.gotoAndStop("gamewin");
            gameState = 3;
         }
         addLevelScores();
         mc_messageF.mc_message.levelTime = getTimeString(levelTimeCounter);
         mc_messageF.mc_message.commonTime = getTimeString(timeCounter);
         mc_messageF.mc_message.scores = scores;
         bikeSync.mc_bike.mc.mc_body_man.mc.stopAnim();
         bikeSync.mc_bike.mc.mc_body_man.mc.stopMCAnim();
         return;
      }
      var _loc2 = {x: 0, y: 0};
      var _loc4 = bikeSync.mc_bike.mc.mc_body_man.mc.mc.h;
      _loc2.x = _loc4.p._x;
      _loc2.y = _loc4.p._y;
      _loc4.localToGlobal(_loc2);
      if(mc_level.mc.mc_hit.hitTest(_loc2.x, _loc2.y, true))
      {
         eval("_root").setBright(eval("_root").bikeSync.mc_bike, 0);
         loose();
         return;
      }
      _loc4 = bikeSync.mc_bike.mc.mc_body_man.mc.mc.b;
      _loc2.x = _loc4.p._x;
      _loc2.y = _loc4.p._y;
      _loc4.localToGlobal(_loc2);
      if(mc_level.mc.mc_hit.hitTest(_loc2.x, _loc2.y, true))
      {
         eval("_root").setBright(eval("_root").bikeSync.mc_bike, 0);
         loose();
         return;
      }
      _loc4 = bikeSync.mc_bike.mc.mc_body_man.mc.mc.l;
      _loc2.x = _loc4.p._x;
      _loc2.y = _loc4.p._y;
      _loc4.localToGlobal(_loc2);
      if(mc_level.mc.mc_hit.hitTest(_loc2.x, _loc2.y, true))
      {
         eval("_root").setBright(eval("_root").bikeSync.mc_bike, 0);
         loose();
      }
   }
}
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
// a time in milliseconds as "mm:ss", each part padded to two digits
// registers: r1 = whole seconds (secs), r2 = whole minutes (mins), r3 = the minutes text (minText), r4 = the seconds text (secText)
function getTimeString(time)
{
   var secs = Math.round(time / 1000);
   var mins = Math.floor(secs / 60);
   secs -= mins * 60;
   var minText;
   var secText;
   if(secs < 10)
   {
      secText = "0" + secs;
   }
   else
   {
      secText = "" + secs;
   }
   if(mins < 10)
   {
      minText = "0" + mins;
   }
   else
   {
      minText = "" + mins;
   }
   // the bytes evaluate the result once and discard it before returning it; probably a
   // statement whose call was stripped at publish (a trace), uncertain
   minText + ":" + secText;
   return minText + ":" + secText;
}
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
// reset the level's moving parts: remove every clip named in _root.bulletArray, then put the
// bomb and the helicopter back to their starting state
// !FAKE: the author wrote _root; eval("_root") keeps the original DefineFunction, which reads _root by name
function clearStuff()
{
   eval("_root").arrdeactivate = true;
   var tlen = eval("_root").bulletArray.length;
   if(tlen > 0)
   {
      j = 0;
      while(j < tlen)
      {
         if(eval("_root").bulletArray[j] != "")
         {
            eval("_root." + eval("_root").bulletArray[j])._alpha = 0;
            eval("_root." + eval("_root").bulletArray[j]).gotoAndStop(39);
            removeMovieClip(eval("_root." + eval("_root").bulletArray[j]));
         }
         j++;
      }
   }
   eval("_root").bulletArray = new Array();
   eval("_root").arrdeactivate = false;
   eval("_root").bikedartctr = 0;
   eval("_root").bomb._alpha = 0;
   eval("_root").dropbomb = false;
   eval("_root").bomb.gotoAndStop(1);
   eval("_root").heliactivate = false;
   eval("_root").helicounter = 1;
   eval("_root").helicop._x = 786.4;
   eval("_root").helicop.rotation = 0;
   eval("_root").helicop._y = 58.4;
   eval("_root").setBright(eval("_root").helicop, 0);
   eval("_root").setBright(eval("_root").bikeSync.mc_bike, 0);
   eval("_root").helidestroy = false;
}
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
// the unit vector from the bike's back wheel to its front wheel, turned a quarter
// turn to (-y, x): the normal to the line through the two wheels
// registers: r1 = the vector returned (n), r2 = its x before the turn (oldX)
function calcBikeNVector()
{
   var n;
   n = bikeSync.mc_forward_wheel.particle.pos.minusNew(bikeSync.mc_back_wheel.particle.pos);
   n.normalize();
   var oldX;
   oldX = n.x;
   n.x = - n.y;
   n.y = oldX;
   return n;
}
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

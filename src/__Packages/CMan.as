// the man: a clip that leans left and right on the arrow keys (key codes 37 and 39),
// playing an ANIM_FRAMES-frame animation each way
class CMan extends MovieClip
{
   var mc;
   var state;
   var stopFlag;
   static var LEFT_BUTTON = 37;
   static var RIGHT_BUTTON = 39;
   static var ANIM_FRAMES = 7;
   // the man character's constructor: clear its stop flag and reset its state
   function CMan()
   {
      super();
      this.stopFlag = false;
      this.state = 0;
   }
   // stops the man's animation: sets the flag the enterFrame handler checks
   function stopAnim()
   {
      this.stopFlag = true;
   }
   function stopMCAnim()
   {
      this.mc.stop();
   }
   // restart the man's animation: clear the flag that stopAnim set
   function startAnim()
   {
      this.stopFlag = false;
   }
   // each frame, unless stopAnim has set stopFlag: a held arrow key leans the man that way;
   // with neither key held, a lean in progress or held (1, 2 left; 4, 5 right) starts its return
   // registers: r2 = the alias of this (man)
   function onEnterFrame()
   {
      var man = this;
      if(man.stopFlag)
      {
         return;
      }
      if(Key.isDown(CMan.LEFT_BUTTON))
      {
         man.toLeft();
         return;
      }
      if(Key.isDown(CMan.RIGHT_BUTTON))
      {
         man.toRight();
         return;
      }
      if(man.state == 1 || man.state == 2)
      {
         man.fromLeft();
         return;
      }
      if(man.state == 4 || man.state == 5)
      {
         man.fromRight();
      }
   }
   // the left key held: from rest (0) the lean starts (1); from the left return (3) it restarts at
   // the frame mirroring the return's; from a right lean (4, 5) the right return starts (6)
   // registers: r2 = the alias of this (man), r3 = the return's current frame (frame)
   function toLeft()
   {
      var man = this;
      var frame;
      if(man.state == 0)
      {
         man.state = 1;
         man.gotoAndStop("toLeft");
         man.state = 1;
         return;
      }
      if(man.state == 3)
      {
         frame = man.mc._currentframe;
         man.gotoAndStop("toLeft");
         man.mc.gotoAndPlay(CMan.ANIM_FRAMES - frame + 1);
         man.state = 1;
         return;
      }
      if(man.state == 4 || man.state == 5)
      {
         man.fromRight();
         man.state = 6;
      }
   }
   // the right key held: from rest (0) the lean starts (4; the 1 written first is toLeft's, probably
   // left from a copy); from the right return (6) it restarts mirrored; from a left lean (1, 2) the left return starts (3)
   // registers: r2 = the alias of this (man), r3 = the return's current frame (frame)
   function toRight()
   {
      var man = this;
      var frame;
      if(man.state == 0)
      {
         man.state = 1;
         man.gotoAndStop("toRight");
         man.state = 4;
         return;
      }
      if(man.state == 6)
      {
         frame = man.mc._currentframe;
         man.gotoAndStop("toRight");
         man.mc.gotoAndPlay(CMan.ANIM_FRAMES - frame + 1);
         man.state = 4;
         return;
      }
      if(man.state == 1 || man.state == 2)
      {
         man.fromLeft();
         man.state = 3;
      }
   }
   // back from the left lean (state 3; endMove turns 3 into 0): from state 1, mid-lean, the
   // return animation starts at the frame mirroring the lean's (ANIM_FRAMES - frame + 1); from 2 at its start
   // registers: r2 = the alias of this (man), r3 = the lean's current frame (frame)
   function fromLeft()
   {
      var man = this;
      var frame;
      if(man.state == 1)
      {
         frame = man.mc._currentframe;
         man.gotoAndStop("fromLeft");
         man.mc.gotoAndPlay(CMan.ANIM_FRAMES - frame + 1);
         man.state = 3;
         return;
      }
      if(man.state == 2)
      {
         man.gotoAndStop("fromLeft");
         man.state = 3;
      }
   }
   // back from the right lean (state 6; endMove turns 6 into 0): from state 4, mid-lean, the
   // return animation starts at the frame mirroring the lean's (ANIM_FRAMES - frame + 1); from 5 at its start
   // registers: r2 = the alias of this (man), r3 = the lean's current frame (frame)
   function fromRight()
   {
      var man = this;
      var frame;
      if(man.state == 4)
      {
         frame = man.mc._currentframe;
         man.gotoAndStop("fromRight");
         man.mc.gotoAndPlay(CMan.ANIM_FRAMES - frame + 1);
         man.state = 6;
         return;
      }
      if(man.state == 5)
      {
         man.gotoAndStop("fromRight");
         man.state = 6;
      }
   }
   // a move's animation ended: 1 holds at the "left" frame as 2, 4 at "right" as 5, and the
   // returns 3 and 6 go back to state 0 on "stay"
   // registers: r2 = the alias of this (man)
   function endMove()
   {
      var man = this;
      if(man.state == 1)
      {
         man.gotoAndStop("left");
         man.state = 2;
         return;
      }
      if(man.state == 3)
      {
         man.state = 0;
         man.gotoAndStop("stay");
         return;
      }
      if(man.state == 4)
      {
         man.state = 5;
         man.gotoAndStop("right");
         return;
      }
      if(man.state == 6)
      {
         man.state = 0;
         man.gotoAndStop("stay");
      }
   }
}

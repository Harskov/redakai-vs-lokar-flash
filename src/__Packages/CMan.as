// @reference Packages_CMan_main
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
// @reference CMan.onEnterFrame
// @reference CMan.toLeft
// @reference CMan.toRight
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
// @reference CMan.endMove

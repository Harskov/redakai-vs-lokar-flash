// @reference Packages_CMan_main
// the man character's constructor: clear its stop flag and reset its state
function CMan()
{
   super();
   this.stopFlag = false;
   this.state = 0;
}
// @reference CMan.stopAnim
function stopMCAnim()
{
   this.mc.stop();
}
// @reference CMan.startAnim
// @reference CMan.onEnterFrame
// @reference CMan.toLeft
// @reference CMan.toRight
// @reference CMan.fromLeft
// @reference CMan.fromRight
// @reference CMan.endMove

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
// @reference CMan.fromLeft
// @reference CMan.fromRight
// @reference CMan.endMove

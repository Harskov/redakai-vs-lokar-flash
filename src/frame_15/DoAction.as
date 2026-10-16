// @reference frame_15_DoAction_main
// while heliactivate is set: the bomb goes to its release point under helicop (34.6 down,
// 10.1 to the left of its origin), back to frame 1 at full alpha, and dropbomb starts its fall
function firebomb()
{
   if(_root.heliactivate == true)
   {
      _root.bomb._y = _root.helicop._y + 34.6;
      _root.bomb._x = _root.helicop._x - 10.1;
      _root.bomb.gotoAndStop(1);
      _root.bomb._alpha = 100;
      _root.delaybomb = 0;
      _root.dropbomb = true;
   }
}
// a clip's brightness via a color matrix that adds newVal to each RGB channel
// registers: r1 = the color matrix (matrix)
function setBright(mc, newVal)
{
   var matrix = [1,0,0,0,newVal,0,1,0,0,newVal,0,0,1,0,newVal,0,0,0,1,0];
   mc.filters = [new flash.filters.ColorMatrixFilter(matrix)];
}

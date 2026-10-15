// @reference frame_15_DoAction_main
// @reference firebomb
// a clip's brightness via a color matrix that adds newVal to each RGB channel
// registers: r1 = the color matrix (matrix)
function setBright(mc, newVal)
{
   var matrix = [1,0,0,0,newVal,0,1,0,0,newVal,0,0,1,0,newVal,0,0,0,1,0];
   mc.filters = [new flash.filters.ColorMatrixFilter(matrix)];
}

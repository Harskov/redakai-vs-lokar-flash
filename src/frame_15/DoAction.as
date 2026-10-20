// the `game` frame: the intro loop and the button sound start, no lives left goes to
// `gameover`, level is taken from lvls, and the score carried over is shown
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
stopAllSounds();
_root.intro.start(0, 9999);
this.stop();
var btnon = new Sound();
btnon.attachSound("btnon");
_root.btnon.start(0, 99);
btnon.setVolume(5);
intro.setVolume(90);
_root.scoress = _root.levelscore;
if(lifee == 0)
{
   _root.gotoAndStop("gameover");
}
if(lvls == 1)
{
   level = 1;
}
if(lvls == 2)
{
   level = 2;
}
// level 3 is tested twice in the original
if(lvls == 3)
{
   level = 3;
}
if(lvls == 3)
{
   level = 3;
}
if(lvls == 4)
{
   level = 4;
}
if(lvls == 5)
{
   level = 5;
}
if(lvls == 6)
{
   level = 6;
}
if(lvls == 7)
{
   level = 7;
}
if(lvls == 8)
{
   level = 8;
}
if(lvls == 9)
{
   level = 9;
}
if(lvls == 10)
{
   level = 10;
}
if(lvls == 11)
{
   level = 11;
}
if(lvls == 12)
{
   level = 12;
}
if(lvls == 13)
{
   level = 13;
}
if(lvls == 14)
{
   level = 14;
}
if(lvls == 15)
{
   level = 15;
}
bikedark = new Array(-30, -40, -90);
bikedartctr = 0;
helibulletctr = 0;
_root.txtscore.text = _root.tscore;
_root.mscore = _root.tscore;

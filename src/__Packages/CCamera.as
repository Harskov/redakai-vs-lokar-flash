// the camera's view, 500 by 400 (the stage is 700 by 500); process puts the target at its centre
class CCamera
{
   static var SCREEN_WIDTH = 500;
   static var SCREEN_HEIGHT = 400;
   static var SCREEN_WIDTH2 = CCamera.SCREEN_WIDTH / 2;
   static var SCREEN_HEIGHT2 = CCamera.SCREEN_HEIGHT / 2;
   function CCamera()
   {
   }
   // registers: r2 = the alias of this (cam)
   // the camera starts on the two movies it watches, then takes its first update
   function init(targetMovie_, levelMovie_)
   {
      var cam = this;
      cam.targetMovie = targetMovie_;
      cam.levelMovie = levelMovie_;
      cam.process();
   }
   // registers: r2 = the alias of this (cam), r3 = the target's position in levelMovie's parent (pt)
   // scrolls levelMovie so that the target sits at the view's centre, in whole pixels, held at the
   // level's left, right and top edges
   function process()
   {
      var cam = this;
      var pt = {x:cam.targetMovie._x, y:cam.targetMovie._y};
      cam.targetMovie._parent.localToGlobal(pt);
      cam.levelMovie._parent.globalToLocal(pt);
      cam.levelMovie._x += CCamera.SCREEN_WIDTH2 - pt.x;
      cam.levelMovie._y += CCamera.SCREEN_HEIGHT2 - pt.y;
      cam.levelMovie._x = Math.round(cam.levelMovie._x);
      cam.levelMovie._y = Math.round(cam.levelMovie._y);
      if(cam.levelMovie._x > 0)
      {
         cam.levelMovie._x = 0;
      }
      else if(cam.levelMovie._x + cam.levelMovie._width < CCamera.SCREEN_WIDTH)
      {
         cam.levelMovie._x = CCamera.SCREEN_WIDTH - cam.levelMovie._width;
      }
      if(cam.levelMovie._y < 0)
      {
         cam.levelMovie._y = 0;
      }
   }
}

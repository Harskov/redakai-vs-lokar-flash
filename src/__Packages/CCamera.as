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
   function process()
   { /* @reference CCamera.process */ }
}

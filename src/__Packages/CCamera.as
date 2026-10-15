// @reference Packages_CCamera_main
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
// @reference CCamera.process

// @reference DefineSprite_205_frame_2_DoAction_main
// onEnterFrame handler: the sprite holds on frame 1 until the main timeline's
// `rotates` reaches 53, then it stops
onEnterFrame = function()
{
   if(_root.rotates == 53)
   {
      stop();
   }
   else
   {
      gotoAndStop(1);
   }
};

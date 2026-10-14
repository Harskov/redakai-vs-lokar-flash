// @reference DefineSprite_205_frame_2_DoAction_main
// frame 1's counterpart: back to frame 1 until the main timeline's `rotates`
// reaches 53, then the sprite stays on this frame
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

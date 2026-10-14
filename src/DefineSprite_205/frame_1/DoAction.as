// @reference DefineSprite_205_frame_1_DoAction_main
// the main timeline's `rotates` counter picks the frame: on 53 the sprite moves on,
// otherwise it holds where it is
onEnterFrame = function()
{
   if(_root.rotates == 53)
   {
      gotoAndStop(2);
   }
   else
   {
      stop();
   }
};

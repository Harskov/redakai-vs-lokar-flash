// the main timeline's `rotates` counter picks the frame: on 53 the sprite moves on,
// otherwise it holds where it is
stop();
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

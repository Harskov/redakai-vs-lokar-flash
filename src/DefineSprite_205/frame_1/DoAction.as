// hold frame 1; no script writes _root.rotates, so what sets it to 53 is not known
stop();
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

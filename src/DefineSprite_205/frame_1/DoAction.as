// hold frame 1; the handler moves on to frame 2 when _root.rotates is 53 (no script
// writes rotates, so what sets it is not known)
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

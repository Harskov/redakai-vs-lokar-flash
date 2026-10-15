// frame 1's counterpart: hold frame 2; the handler goes back to frame 1 once
// _root.rotates is no longer 53
stop();
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

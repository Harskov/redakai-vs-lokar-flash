// frame 2's counterpart: hold this frame once the main timeline's `rotates`
// reaches 53, else back to frame 1
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

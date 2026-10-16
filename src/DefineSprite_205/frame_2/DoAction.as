// hold frame 2: frame 1's script with the two branches swapped
stop();
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

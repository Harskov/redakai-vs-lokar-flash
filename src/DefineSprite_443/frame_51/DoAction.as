// the end of the crash animation: one life fewer, then the level again
onEnterFrame = function()
{
   _root.lifee -= 1;
   _root.replay();
};

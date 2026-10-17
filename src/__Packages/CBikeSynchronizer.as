// the class script for CBikeSynchronizer: register the class on _global once, then put
// init, setParticles and process on its prototype
class CBikeSynchronizer
{
   // four zero vectors: a direction and a position each for f and b (probably the forward and
   // back wheels, the class's mc_forward_wheel and mc_back_wheel)
   // registers: r2 = the alias of this (sync)
   function CBikeSynchronizer()
   {
      var sync = this;
      sync.fdir = new CVector2D(0, 0);
      sync.fpos = new CVector2D(0, 0);
      sync.bdir = new CVector2D(0, 0);
      sync.bpos = new CVector2D(0, 0);
   }
   // attaches the two wheel clips and the body to mc_container, puts the body at (sX, sY), then sets
   // each wheel on its mc_s_wheel_* marker of the body, 10 pixels further out, in the container's space
   // registers: r2 = the alias of this (sync), r4 = the alias of mc_container (container), r3 = the point carried between the clips' spaces (pt)
   function init(mc_container, sX, sY)
   {
      var sync = this;
      var container = mc_container;
      var pt = {x:0, y:0};
      sync.mc_back_wheel = container.attachMovie("lib_back_wheel", "back_w", 2);
      sync.mc_forward_wheel = container.attachMovie("lib_forward_wheel", "forward_w", 1);
      sync.mc_bike = container.attachMovie("lib_bike_body", "body", 3);
      sync.mc_bike._x = sX;
      sync.mc_bike._y = sY;
      pt.x = sync.mc_bike.mc.mc_s_wheel_back._x - 10;
      pt.y = sync.mc_bike.mc.mc_s_wheel_back._y;
      sync.mc_bike.mc.localToGlobal(pt);
      sync.mc_bike._parent.globalToLocal(pt);
      sync.mc_back_wheel._x = pt.x;
      sync.mc_back_wheel._y = pt.y;
      pt.x = sync.mc_bike.mc.mc_s_wheel_forward._x + 10;
      pt.y = sync.mc_bike.mc.mc_s_wheel_forward._y;
      sync.mc_bike.mc.localToGlobal(pt);
      sync.mc_bike._parent.globalToLocal(pt);
      sync.mc_forward_wheel._x = pt.x;
      sync.mc_forward_wheel._y = pt.y;
   }
   function setParticles(pBody_, pBWheel_, pFWheel_)
   { /* @reference CBikeSynchronizer.setParticles */ }
   function process()
   { /* @reference CBikeSynchronizer.process */ }
}

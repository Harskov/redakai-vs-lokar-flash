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
   // keeps the three particles and takes the body clip's geometry once, from its marker clips:
   // the front fork's direction and where it crosses the clip's y = 0, and the top of the back
   // spring, in mc_body_man's and mc's space
   // registers: r2 = the alias of this (sync)
   function setParticles(pBody_, pBWheel_, pFWheel_)
   {
      var sync = this;
      sync.pBody = pBody_;
      sync.pBWheel = pBWheel_;
      sync.pFWheel = pFWheel_;
      sync.fdir.reinit(sync.mc_bike.mc.mc_f_point._x - sync.mc_bike.mc.mc_s_wheel_forward._x, sync.mc_bike.mc.mc_f_point._y - sync.mc_bike.mc.mc_s_wheel_forward._y);
      sync.fdir.normalize();
      sync.fpos.x = sync.mc_bike.mc.mc_f_spring._x + sync.fdir.x * (-sync.mc_bike.mc.mc_f_spring._y) / sync.fdir.y;
      sync.fpos.x -= sync.mc_bike.mc.mc_body_man._x;
      sync.bpos.reinit(sync.mc_bike.mc.mc_b_spring.mc_top._x, sync.mc_bike.mc.mc_b_spring.mc_top._y);
      sync.mc_bike.mc.mc_b_spring.localToGlobal(sync.bpos);
      sync.bdir.reinit(sync.bpos.x, sync.bpos.y);
      sync.mc_bike.mc.mc_body_man.globalToLocal(sync.bpos);
      sync.mc_bike.mc.globalToLocal(sync.bdir);
      sync.bdir.x -= sync.mc_bike.mc.mc_b_spring._x;
      sync.bdir.y -= sync.mc_bike.mc.mc_b_spring._y;
   }
   // puts the body clip on the particles: mc_bike at pBody, turned along the wheelbase; the front spring
   // clip on the front wheel, with mc_body_man slid along x to keep fpos on the fork's line; the back
   // spring clip on the back wheel, turned by the angle between bdir and its direction to bpos now
   // registers: r2 = the alias of this (sync), r3 = the point carried between the clips' spaces (pt), r4 = the wheelbase and then the back spring's direction (dir), r5 = the slide of mc_body_man along x (dx)
   function process()
   {
      var sync = this;
      var pt = {x:0, y:0};
      var dir;
      sync.mc_bike._x = sync.pBody.pos.x;
      sync.mc_bike._y = sync.pBody.pos.y;
      dir = sync.pFWheel.pos.minusNew(sync.pBWheel.pos);
      sync.mc_bike._rotation = Math.atan2(dir.y, dir.x) * 180 / 3.141593;
      pt.x = sync.pFWheel.pos.x;
      pt.y = sync.pFWheel.pos.y;
      sync.mc_bike._parent.localToGlobal(pt);
      sync.mc_bike.mc.globalToLocal(pt);
      sync.mc_bike.mc.mc_f_spring._x = pt.x;
      sync.mc_bike.mc.mc_f_spring._y = pt.y;
      var dx = pt.x + sync.fdir.x * (-pt.y) / sync.fdir.y - sync.mc_bike.mc.mc_body_man._x - sync.fpos.x;
      sync.mc_bike.mc.mc_body_man._x += dx;
      pt.x = sync.mc_bike.mc.mc_f_spring.mc_spring._x;
      pt.y = sync.mc_bike.mc.mc_f_spring.mc_spring._y;
      sync.mc_bike.mc.mc_f_spring.localToGlobal(pt);
      sync.mc_bike.mc.globalToLocal(pt);
      pt.x = sync.pBWheel.pos.x;
      pt.y = sync.pBWheel.pos.y;
      sync.mc_bike._parent.localToGlobal(pt);
      sync.mc_bike.mc.globalToLocal(pt);
      sync.mc_bike.mc.mc_b_spring._x = pt.x;
      sync.mc_bike.mc.mc_b_spring._y = pt.y;
      dir.reinit(sync.bpos.x, sync.bpos.y);
      sync.mc_bike.mc.mc_body_man.localToGlobal(dir);
      sync.mc_bike.mc.globalToLocal(dir);
      dir.x -= sync.mc_bike.mc.mc_b_spring._x;
      dir.y -= sync.mc_bike.mc.mc_b_spring._y;
      sync.mc_bike.mc.mc_b_spring._rotation = (dir.getUgol() - sync.bdir.getUgol()) * 180 / 3.141593;
   }
}

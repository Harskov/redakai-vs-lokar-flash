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
   function init(mc_container, sX, sY)
   { /* @reference CBikeSynchronizer.init */ }
   function setParticles(pBody_, pBWheel_, pFWheel_)
   { /* @reference CBikeSynchronizer.setParticles */ }
   function process()
   { /* @reference CBikeSynchronizer.process */ }
}

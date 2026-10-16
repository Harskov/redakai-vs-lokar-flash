// the class script for CParticle: register the class on _global once, then put
// verlet on its prototype
class CParticle
{
   // a particle's state: position, previous position for the Verlet step, mass, acceleration and its clip
   // registers: r2 = the alias of this (me)
   function CParticle(x_, y_, mass_)
   {
   var me = this;
   me.pos = new CVector2D(x_, y_);
   me.prevPos = me.pos.duplicate();
   me.mass = mass_;
   me.acc = new CVector2D(0, 0);
   me.mc = null;
}
   function verlet(dTime, koeffDamp)
   { /* @reference CParticle.verlet */ }
}

// the CParticle class script: registers the class, its constructor and verlet on the prototype, and hides the prototype's new members with ASSetPropFlags
class CParticle
{
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

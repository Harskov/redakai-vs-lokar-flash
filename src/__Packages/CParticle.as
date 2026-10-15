// @reference Packages_CParticle_main
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
// @reference CParticle.verlet

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
   // the Verlet step: pos moves by its last displacement, damped by koeffDamp, plus acc over dTime;
   // the old pos becomes prevPos, and the clip, when there is one, follows
   // registers: r2 = the alias of this (me), r3 = the copy of pos before the step (oldPos)
   function verlet(dTime, koeffDamp)
   {
      var me = this;
      var oldPos = me.pos.duplicate();
      me.pos.x += (me.pos.x - me.prevPos.x) * koeffDamp + me.acc.x * dTime;
      me.pos.y += (me.pos.y - me.prevPos.y) * koeffDamp + me.acc.y * dTime;
      oldPos.copyTo(me.prevPos);
      // !FAKE: the author wrote if(me.mc != null); the doubled parentheses keep the double Not before the branch
      if((me.mc != null))
      {
         me.mc._x = me.pos.x;
         me.mc._y = me.pos.y;
      }
   }
}

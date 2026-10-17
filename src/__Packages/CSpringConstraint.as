// the class script for CSpringConstraint: register the class on _global once, then put
// resolve on its prototype
class CSpringConstraint
{
   // a spring between particles p1 and p2 with its two stiffness factors (compression and
   // stretch); its rest length relaxLen is the particles' distance when it is made
   // registers: r2 = the alias of this (spring), r3 = the vector from p2 to p1 (d)
   function CSpringConstraint(p1_, p2_, koeffStiffPress_, koeffStiffStretch_)
   {
      var spring = this;
      spring.p1 = p1_;
      spring.p2 = p2_;
      spring.koeffStiffPress = koeffStiffPress_;
      spring.koeffStiffStretch = koeffStiffStretch_;
      var d = new CVector2D(spring.p1.pos.x - spring.p2.pos.x, spring.p1.pos.y - spring.p2.pos.y);
      spring.relaxLen = d.modul();
   }
   // pull p1 and p2 back toward relaxLen along the line between them; each moves by half of
   // (1 + the other's share of the total mass), so the lighter one moves further; stretch and
   // compression have their own stiffness, and dTime is not read
   // registers: r2 = the alias of this (spring), r3 = the vector from p2 to p1 (d), r5 = its length (len), r6 = the relative error to relaxLen (diff), r4 = the stiffness that applies (stiff)
   function resolve(dTime)
   {
      var spring = this;
      var d = new CVector2D(spring.p1.pos.x - spring.p2.pos.x, spring.p1.pos.y - spring.p2.pos.y);
      var len = d.modul();
      var diff = (spring.relaxLen - len) / len;
      d.mult(diff);
      var stiff;
      if(len > spring.relaxLen)
      {
         stiff = spring.koeffStiffStretch;
      }
      else
      {
         stiff = spring.koeffStiffPress;
      }
      spring.p2.pos.x -= d.x * (spring.p1.mass / (spring.p1.mass + spring.p2.mass) + 1) / 2 * stiff;
      spring.p2.pos.y -= d.y * (spring.p1.mass / (spring.p1.mass + spring.p2.mass) + 1) / 2 * stiff;
      spring.p1.pos.x += d.x * (spring.p2.mass / (spring.p1.mass + spring.p2.mass) + 1) / 2 * stiff;
      spring.p1.pos.y += d.y * (spring.p2.mass / (spring.p1.mass + spring.p2.mass) + 1) / 2 * stiff;
   }
}

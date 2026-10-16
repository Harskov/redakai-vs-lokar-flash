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
   function resolve(dTime)
   { /* @reference CSpringConstraint.resolve */ }
}

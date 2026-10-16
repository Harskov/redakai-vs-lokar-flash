// the scrolling backdrop: two clips side by side that process slides against the level's x
class CBack
{
   static var SCREEN_WIDTH = 500;
   function CBack()
   {
   }
   // the object's setup: stores the three arguments on this
   // registers: r2 = the alias of this (back)
   function init(mc1_, mc2_, scaleFactor_)
   {
      var back = this;
      back.mc1 = mc1_;
      back.mc2 = mc2_;
      back.scaleFactor = scaleFactor_;
   }
   // scrolls the two clips against levelX: the offset is levelX over scaleFactor, wrapped to
   // mc1's width; mc1 moves left by it and mc2 sits after mc1, overlapping it by one pixel
   // registers: r2 = the alias of this (back), r3 = the scroll offset (offset)
   function process(levelX)
   {
      var back = this;
      var offset = levelX;
      offset = Math.abs(Math.round(offset) / back.scaleFactor) % back.mc1._width;
      back.mc1._x = - offset;
      back.mc2._x = back.mc1._x + back.mc1._width - 1;
   }
}

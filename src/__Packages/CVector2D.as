// a 2D vector (x, y) and its arithmetic: the "New" methods return a new vector, the others
// change this one; getUgol is the angle and modul the length (Russian "ugol", "modul")
class CVector2D
{
   var x;
   var y;
   // the constructor: the vector's two components, as the caller passes them
   function CVector2D(x_, y_)
   {
      this.x = x_;
      this.y = y_;
   }
   // sets both components in place, from the values the caller passes
   function reinit(x_, y_)
   {
      this.x = x_;
      this.y = y_;
   }
   // the vector's angle (Russian "ugol"), in the order atan2 expects: y then x
   function getUgol()
   {
      return Math.atan2(this.y, this.x);
   }
   // a new vector with this one's components
   function duplicate()
   {
      return new CVector2D(this.x, this.y);
   }
   // the vector's components copied into another vector, in place
   function copyTo(v)
   {
      v.x = this.x;
      v.y = this.y;
   }
   // the vector's components each reduced by the other's, in place
   function minus(v)
   {
      this.x -= v.x;
      this.y -= v.y;
   }
   // the difference of this vector and v as a new vector
   function minusNew(v)
   {
      return new CVector2D(this.x - v.x, this.y - v.y);
   }
   // registers: r2 = the alias of this (vec), r3 = the vector's length (len)
   // scales the vector to unit length, in place, by its own length
   function normalize()
   {
      var vec = this;
      var len = Math.sqrt(vec.x * vec.x + vec.y * vec.y);
      vec.x /= len;
      vec.y /= len;
   }
   // a new vector with both components negated
   function reverseNew()
   {
      return new CVector2D(-this.x, -this.y);
   }
   // the dot product with another vector
   function scalar(v)
   {
      return this.x * v.x + this.y * v.y;
   }
   // the vector's length (Russian "modul"); the original computes it twice and drops the first result
   // registers: r2 = the alias of this (vec)
   function modul()
   {
      var vec = this;
      Math.sqrt(vec.x * vec.x + vec.y * vec.y);
      return Math.sqrt(vec.x * vec.x + vec.y * vec.y);
   }
   // reflects the vector off a surface with normal n: rotate into the normal's frame, flip the x component, rotate back
   // registers: r2 = the alias of this (v), r3 = the normal's angle from atan2 (a)
   function reflectFromNormal(n)
   {
      var v = this;
      var a = Math.atan2(n.y, n.x);
      v.rotate(-a);
      v.x = -v.x;
      v.rotate(a);
   }
   // rotates the vector in place by the angle u, in radians (the angle goes to Math.cos and Math.sin)
   // registers: r2 = the angle (a), r3 = the alias of this (vec), r4 = the old x (oldX), r5 = the old y (oldY)
   function rotate(u)
   {
      var a = u;
      var vec = this;
      var oldX = vec.x;
      var oldY = vec.y;
      vec.x = oldX * Math.cos(a) - oldY * Math.sin(a);
      vec.y = oldX * Math.sin(a) + oldY * Math.cos(a);
   }
   // a new vector: this one rotated by the angle u, in radians; the original builds it twice and drops the first
   // registers: r2 = the angle (a), r3 = the alias of this (vec)
   function rotateNew(u)
   {
      var a = u;
      var vec = this;
      new CVector2D(vec.x * Math.cos(a) - vec.y * Math.sin(a), vec.x * Math.sin(a) + vec.y * Math.cos(a));
      return new CVector2D(vec.x * Math.cos(a) - vec.y * Math.sin(a), vec.x * Math.sin(a) + vec.y * Math.cos(a));
   }
   // scales both components in place by the caller's factor
   function mult(k)
   {
      this.x *= k;
      this.y *= k;
   }
   // a new vector with both components scaled by k
   function multNew(k)
   {
      return new CVector2D(this.x * k, this.y * k);
   }
   // adds v's components to this vector's, in place
   function plus(v)
   {
      this.x += v.x;
      this.y += v.y;
   }
   // the sum of this vector and v as a new vector, both components added
   function plusNew(v)
   {
      return new CVector2D(this.x + v.x, this.y + v.y);
   }
   // the signed distance from this point to the line through p1 and p2: the line as a*x + b*y + c,
   // scaled by the length of (a, b); the original computes the result twice and drops the first
   // registers: r4 = the alias of p1 (q), r3 = the line's x coefficient (a), r2 = the line's y coefficient (b), r5 = the line's constant (c), r6 = the length of (a and b) (len)
   function getDistanceTo(p1, p2)
   {
      var q = p1;
      var a = q.y - p2.y;
      var b = p2.x - q.x;
      var c = q.x * (p2.y - q.y) - q.y * (p2.x - q.x);
      var len = Math.sqrt(a * a + b * b);
      a /= len;
      b /= len;
      c /= len;
      a * this.x + b * this.y + c;
      return a * this.x + b * this.y + c;
   }
}

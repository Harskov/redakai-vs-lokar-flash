// @reference Packages_CVector2D_main
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
// the vector's length (Russian "modul")
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
// @reference CVector2D.rotate
// @reference CVector2D.rotateNew
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
// @reference CVector2D.getDistanceTo

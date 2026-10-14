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
// @reference CVector2D.minusNew
// @reference CVector2D.normalize
// @reference CVector2D.reverseNew
// the dot product with another vector
function scalar(v)
{
   return this.x * v.x + this.y * v.y;
}
// @reference CVector2D.modul
// @reference CVector2D.reflectFromNormal
// @reference CVector2D.rotate
// @reference CVector2D.rotateNew
// scales both components in place by the caller's factor
function mult(k)
{
   this.x *= k;
   this.y *= k;
}
// @reference CVector2D.multNew
// @reference CVector2D.plus
// the sum of this vector and v as a new vector, both components added
function plusNew(v)
{
   return new CVector2D(this.x + v.x, this.y + v.y);
}
// @reference CVector2D.getDistanceTo

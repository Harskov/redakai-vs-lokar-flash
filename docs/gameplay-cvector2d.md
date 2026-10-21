# gameplay/cvector2d

The 2D vector value type of the physics. Methods ending in `New` return a new vector, the rest change this one in place. Fields and callers: [classes/CVector2D.md](classes/CVector2D.md).

## Functions

- `Packages_CVector2D_main` (matched) — the CVector2D class script: registers the vector class on _global and puts its arithmetic on the prototype
- `CVector2D` (matched) — the vector's constructor: stores x_ and y_ as x and y
- `CVector2D.reinit` (matched) — sets both components in place
- `CVector2D.getUgol` (matched) — the vector's angle in radians (atan2 of y, x); ugol is Russian for angle
- `CVector2D.duplicate` (matched) — a new vector with this one's components
- `CVector2D.copyTo` (matched) — copies this vector's components into v
- `CVector2D.minus` (matched) — subtracts v from this vector in place
- `CVector2D.minusNew` (matched) — this vector minus v, as a new vector
- `CVector2D.normalize` (matched) — scales the vector to unit length in place
- `CVector2D.reverseNew` (matched) — the negated vector, as a new vector
- `CVector2D.scalar` (matched) — the dot product with v
- `CVector2D.modul` (matched) — the vector's length (Russian modul); the bytes compute it twice and drop the first
- `CVector2D.reflectFromNormal` (matched) — reflects the vector in place off a surface with normal n: rotate into the normal's frame, negate x, rotate back
- `CVector2D.rotate` (matched) — rotates the vector in place by u radians
- `CVector2D.rotateNew` (matched) — the vector rotated by u radians
- `CVector2D.mult` (matched) — scales this vector in place by k
- `CVector2D.multNew` (matched) — the vector scaled by k, as a new vector
- `CVector2D.plus` (matched) — adds v to this vector in place
- `CVector2D.plusNew` (matched) — the sum of this vector and v, as a new vector
- `CVector2D.getDistanceTo` (matched) — the signed distance from this point to the line through p1 and p2

## Evidence

- `new CVector2D` appears 14 times in the scripts (classes/CVector2D.md)
- `getUgol` and `modul`: Russian for angle and magnitude; method names are the author's

# gameplay/cvector2d

The 2D vector value type of the physics. Methods ending in `New` return a new vector, the rest change this one in place. Fields and callers: [classes/CVector2D.md](classes/CVector2D.md).

## Functions

- `Packages_CVector2D_main` (not yet matched) — the class definition script
- `CVector2D` (matched) — the vector's constructor: stores x_ and y_ as x and y
- `CVector2D.reinit` (matched) — sets both components in place
- `CVector2D.getUgol` (matched) — the vector's angle in radians (atan2 of y, x); ugol is Russian for angle
- `CVector2D.duplicate` (matched) — a new vector with this one's components
- `CVector2D.copyTo` (matched) — copies this vector's components into v
- `CVector2D.minus` (matched) — subtracts v from this vector in place
- `CVector2D.minusNew` (not yet matched) — this minus v, as a new vector
- `CVector2D.normalize` (not yet matched) — to unit length, in place
- `CVector2D.reverseNew` (not yet matched) — the negated vector
- `CVector2D.scalar` (matched) — the dot product with v
- `CVector2D.modul` (not yet matched) — the length (Russian modul)
- `CVector2D.reflectFromNormal` (not yet matched) — reflects in place about the normal n
- `CVector2D.rotate` (not yet matched) — rotates in place by u radians
- `CVector2D.rotateNew` (not yet matched) — the vector rotated by u radians
- `CVector2D.mult` (matched) — scales this vector in place by k
- `CVector2D.multNew` (not yet matched) — the vector scaled by k
- `CVector2D.plus` (not yet matched) — adds v in place
- `CVector2D.plusNew` (matched) — the sum of this vector and v, as a new vector
- `CVector2D.getDistanceTo` (not yet matched) — the signed distance from this point to the line through p1 and p2

## Evidence

- `new CVector2D` appears 14 times in the scripts (classes/CVector2D.md)
- `getUgol` and `modul`: Russian for angle and magnitude; method names are the author's

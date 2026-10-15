# CVector2D

A two-component vector, the physics' value type (`new CVector2D` appears 14 times in the scripts). The method names are the author's; `ugol` and `modul` are Russian for angle and magnitude. `*New` methods return a new vector; the others change this one in place.

**Prototype.** `class CVector2D` (no base class); fields `x`, `y`, declared in that order and assigned by the constructor from `x_`, `y_`.

**Fields.** `x`, `y`: written by the constructor, `reinit`, and `copyTo` (on its argument); read by every other method.

| Method | Accepted | Callers (confirmed in the scripts) |
|---|---|---|
| `CVector2D(x_, y_)` | yes | every `new CVector2D` |
| `reinit(x_, y_)` | yes | CBikeSynchronizer.setParticles, CBikeSynchronizer.process |
| `getUgol()` | yes | CBikeSynchronizer.process (the rear spring's rotation) |
| `duplicate()` | yes | CParticle (constructor), CParticle.verlet |
| `copyTo(v)` | yes | CParticle.verlet, CWheel.checkCollision, CWheel.pushOut |
| `minus(v)` | yes | none found |
| `scalar(v)` | yes | CWheel.checkCollision |
| `mult(k)` | yes | CSpringConstraint.resolve |
| `plusNew(v)` | yes | CWheel.pushOut |
| `minusNew(v)`, `normalize()`, `reverseNew()`, `reflectFromNormal(n)`, `multNew(k)`, `plus(v)` | yes | see `docs/CODE-MAP.md` |
| `modul`, `rotate`, `rotateNew`, `getDistanceTo` | no | see `docs/CODE-MAP.md` |

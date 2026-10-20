# CSpringConstraint

A spring between two particles of the physics engine: `CParticleEngine.addSpringConstraint` makes one and keeps it in `c_array`, and `CParticleEngine.checkConstraints` calls each one's `resolve(dTime)`.

**Prototype.** `class CSpringConstraint` (no base class); the constructor stores `p1`, `p2`, `koeffStiffPress`, `koeffStiffStretch` (two stiffness factors, probably for compression and stretch; unverified) and sets `relaxLen` to the particles' distance at that moment (`CVector2D.modul` of `p1.pos - p2.pos`).

| Method | Accepted | Callers (confirmed in the scripts) |
|---|---|---|
| `CSpringConstraint(p1_, p2_, koeffStiffPress_, koeffStiffStretch_)` | yes | CParticleEngine.addSpringConstraint |
| `resolve(dTime)` | yes | CParticleEngine.checkConstraints |

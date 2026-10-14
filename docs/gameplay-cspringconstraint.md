# gameplay/cspringconstraint

A spring between two particles, with one stiffness for compression (`koeffStiffPress`) and one for stretch (`koeffStiffStretch`). `resolve` moves both ends toward the rest length `relaxLen`, measured at creation, each weighted by the other's mass.

## Functions

- `Packages_CSpringConstraint_main` (not yet matched) — the class definition script
- `CSpringConstraint` (not yet matched) — the constructor: the two particles, both stiffnesses, relaxLen from modul()
- `CSpringConstraint.resolve` (not yet matched) — the correction toward relaxLen

## Evidence

- three springs in `initLevel`: back-front (0.45, 0.5), back-body (0.45, 0.55), body-front (0.45, 0.7)
- `relaxLen = ...modul()` in the constructor

# gameplay/cback

The parallax background layer: two tiles side by side, scrolled at 1/scaleFactor of the level's x. `initLevel` makes `back1` (grass, factor 1) and `back2` (hill, factor 2); `processGame` calls `process(mc_level.mc._x)` each frame. Fields and callers: [classes/CBack.md](classes/CBack.md).

## Functions

- `Packages_CBack_main` (not yet matched) — the class definition script (the AS2 compiler's _global registration and prototype)
- `CBack` (matched) — the parallax layer's constructor; init() supplies the two tiles and the scale factor
- `CBack.init` (not yet matched) — stores the two tiles and the scale factor
- `CBack.process` (not yet matched) — offsets the first tile by the scaled level x modulo its width and butts the second against it

## Evidence

- `back1.init(...mc_grass.mc1, ...mc2, 1)` and `back2.init(...mc_hill.mc1, ...mc2, 2)` in `initLevel`
- static `SCREEN_WIDTH = 500` in the class

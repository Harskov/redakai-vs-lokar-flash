# gameplay/cback

The parallax background layer: two tiles side by side, scrolled at 1/scaleFactor of the level's x. `initLevel` makes `back1` (grass, factor 1) and `back2` (hill, factor 2); `processGame` calls `process(mc_level.mc._x)` each frame. Fields and callers: [classes/CBack.md](classes/CBack.md).

## Functions

- `Packages_CBack_main` (matched) — the CBack class script: registers the class on _global with SCREEN_WIDTH 500 and puts init and process on its prototype
- `CBack` (matched) — the parallax layer's constructor; init() supplies the two tiles and the scale factor
- `CBack.init` (matched) — stores the backdrop's two tiles (mc1, mc2) and its scale factor; initLevel gives back1 the grass tiles at 1 and back2 the hill tiles at 2
- `CBack.process` (matched) — scrolls the two tiles against the level's x: the offset is levelX over scaleFactor wrapped to mc1's width; mc2 follows mc1 one pixel overlapped

## Evidence

- `back1.init(...mc_grass.mc1, ...mc2, 1)` and `back2.init(...mc_hill.mc1, ...mc2, 2)` in `initLevel`
- static `SCREEN_WIDTH = 500` in the class

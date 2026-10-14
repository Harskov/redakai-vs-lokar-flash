# CBack

A scrolling background layer made of two clips; `initLevel` creates two (`back1` for the grass, `back2` for the hills) with scale factors 1 and 2, and processGame moves both with the level's `_x`.

**Prototype.** `class CBack` (no base class); `static var SCREEN_WIDTH = 500`; instance fields `mc1`, `mc2`, `scaleFactor`, written by `init`.

| Method | Accepted | Callers (confirmed in the scripts) |
|---|---|---|
| `CBack()` | yes | initLevel (`back1`, `back2`) |
| `init(mc1_, mc2_, scaleFactor_)` | no | initLevel |
| `process(levelX)` | no | processGame (`back1.process(mc_level.mc._x)`, `back2.…`) |

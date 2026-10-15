# CCamera

The camera: it moves the level clip so that the target clip (the bike) stays in view. One instance, `objCamera`, created in `initLevel`.

**Prototype.** `class CCamera` (no base class); statics `SCREEN_WIDTH = 500`, `SCREEN_HEIGHT = 400`, `SCREEN_WIDTH2` and `SCREEN_HEIGHT2` (their halves); instance fields `targetMovie`, `levelMovie`, written by `init`.

| Method | Accepted | Callers (confirmed in the scripts) |
|---|---|---|
| `CCamera()` | yes | initLevel (`objCamera = new CCamera()`) |
| `init(targetMovie_, levelMovie_)` | yes | initLevel (`objCamera.init(bikeSync.mc_bike, mc_level.mc)`) |
| `process()` | no | processGame |

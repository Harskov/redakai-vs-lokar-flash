# gameplay/ccamera

Keeps the bike in view: each frame `process` shifts the level clip so the target sits at (250, 200), rounds, and clamps at the level's left and right edges and its top. Fields and callers: [classes/CCamera.md](classes/CCamera.md).

## Functions

- `Packages_CCamera_main` (matched) — the CCamera class script: registers the class with the 500 x 400 view (SCREEN_WIDTH, SCREEN_HEIGHT and their halves) and puts init and process on its prototype
- `CCamera` (matched) — the camera's constructor; init() supplies the followed clip and the level clip
- `CCamera.init` (matched) — stores the followed clip and the level clip, then positions the view once; initLevel passes bikeSync.mc_bike and mc_level.mc
- `CCamera.process` (not yet matched) — the shift, the rounding and the clamps

## Not known

- the class uses a 500 x 400 screen while the stage is 700 x 500 (DOSSIER.md); whether that is deliberate is not known

## Evidence

- `objCamera.init(bikeSync.mc_bike, mc_level.mc)` in `initLevel`
- statics SCREEN_WIDTH 500, SCREEN_HEIGHT 400 and their halves SCREEN_WIDTH2, SCREEN_HEIGHT2

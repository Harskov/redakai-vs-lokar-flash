# Glossary

| Term | Meaning | Evidence |
|---|---|---|
| `gameState` | the play state: 0 playing, 1 lost, 2 level complete, 3 game won, 4 paused | its writers `initLevel`, `resume`, `loose`, `processGame`, `pauseGame` |
| `level` | the level the physics game builds (`mc_level` frame); 1-10 in `nextLevel` | `initLevel`, `nextLevel`, frame 15 |
| `lvls` | the level the menus track (1-15 on the level selection; `gamewin` at 7) | frames 12, 15, 17, 18 |
| `life` / `lifee` | two life counters: `life` (10) is decremented by `loose` and never tested; `lifee` (5) by the crash clip, tested on frame 15 | `gameStart`, `loose`, `DefineSprite_443_frame_51_DoAction.onEnterFrame`, `frame_15_DoAction_main` |
| `scores` / `mscore` / `tscore` / `levelscore` / `scorecard` | the physics game's score (shown in `mc_messageF`) and the menus' running scores | `gameStart`, `loose`, the shot checker, frames 17, 19, 20 |
| `stargeted` | a count `processGame` tests `>= 3` at the finish; `processGame` sets it to 5 just before | `processGame`, `replay`, `nextLevel` |
| `bulletArray` / `kval` / `kfire` | the live shots' names, the next shot's number (1000-1100), the gun's ready flag | `processGame`, `clearStuff`, `resetkfire` |
| `mx1`...`my3` | the gun's aim points on the stage, written by `car1`'s clip actions | gameplay-86.md |
| `helicop`, `bomb`, `crash`, `health_mc`, `score_mc` | frame 15's named clips: helicopter, its bomb, the crash animation, the health meter, the score pop-up | the original's PlaceObject tags |
| `mc_level` | sprite 387; frames `level1`...`level6` each hold one level as `mc` | the original's FrameLabel and PlaceObject tags |
| `mc_hit` | the level's ground clip the wheels and the rider test against | `initLevel`, `CWheel.checkCollision`, `processGame` |
| `mc_fon` | the level's background holder (the grass and hill parallax layers, the random background); fon is Russian for background (a reading) | `initLevel`, `processGame`, sprites 159 and 358 |
| `ugol`, `modul`, `koeff` | angle, magnitude, coefficient: Russian terms in the physics classes' identifiers | `CVector2D.getUgol`, `CVector2D.modul`, `CWheel`, `CSpringConstraint` |
| `zast` | in `zastSoundFlag` and `mc_sloop_zast`: picks the menus' music loop; possibly Russian for title screen (unverified) | `updateSoundLoop`, `newGame`, `gameStart` |
| `logo`, `soundatta`, `main`, `carselection`, `help`, `game`, `reset`, `comple`, `level selection`, `gamewin`, `gameover` | the main timeline's frame labels, frames 10-20 | DOSSIER.md |
| `lib_man`, `lib_bike_body`, `lib_forward_wheel`, `lib_back_wheel`, `bullet_id`, `rocket_id` | export names the code attaches or links to a class | the original's ExportAssets |

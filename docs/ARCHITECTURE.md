# Architecture

How the game works, read from the scripts. Every claim names the function, frame label or instance
name it comes from; where the scripts do not settle a question, the page says so. Function names are
the ledger's (`docs/CODE-MAP.md` maps each to its file); `matched` means the source in `src/` is
accepted, the rest is still the reference line.

## The file

One SWF 9 movie, 700×500 px at 35 fps, 20 frames on the main timeline, 95 AVM1 scripts
(`DOSSIER.md`). The code lives in three places: the main timeline's frame actions (`frame_<n>_DoAction`),
one init action that defines the game's global functions (`DoInitAction`, the init action of
sprite 150, tag 304, on frame 11 `soundatta`; its functions run with `this` as `_root`), and nine AS2 classes under `__Packages` (`CVector2D`, `CParticle`,
`CSpringConstraint`, `CWheel`, `CParticleEngine`, `CBikeSynchronizer`, `CCamera`, `CBack`, `CMan`).
The rest is frame actions inside sprites, mostly a single `stop()`.

## The main timeline (the state machine of the menus)

| Frame | Label | What its scripts do |
|---|---|---|
| 1 | — | the preloader: `frame_1_DoAction.onEnterFrame` sizes the bar from `getBytesLoaded()`; at 100% it plays from frame 10 |
| 10 | `logo` | `frame_10_DoAction_main` creates the sounds (`intro`, `accSnd`, `accLoop`, `pb`, `cra`) and `lifee = 5`; button 124 (`btn1`) zeroes `tscore`/`mscore`, sets `lvls = 1` and plays from 15 |
| 11 | `soundatta` | `frame_11_DoAction_main` holds; no script jumps here, so the way in is not known |
| 12 | `main` | `frame_12_DoAction_main` sets `lvls = 1`, `scores`, `lifee = 5`, `totascores`; buttons 147 (play, from 15) and 148 (help) sit on 11–12 |
| 13 | `carselection` | `frame_13_DoAction_main` stops every sound; nothing in the scripts writes `jeepselection`, the variable the jeep and tyre sprites read |
| 14 | `help` | `frame_14_DoAction_main` stops every sound; reached from button 148 |
| 15 | `game` | the level: `frame_15_DoAction_main` defines `firebomb` and `setBright`, maps `lvls` to `level`, sends the timeline to `gameover` when `lifee == 0` |
| 16 | `reset` | no script; `nextLevel` and `replay` stop here and go straight back to `game` |
| 17 | `comple` | `frame_17_DoAction_main`: `lvls++`, 100 points to `scorecard`, `gamewin` when `lvls == 7`; button 461 restarts through `gameStart` |
| 18 | `level selection` | `frame_18_DoAction.onEnterFrame` unlocks buttons `le1`…`le15` up to `lvls`; each sets `lvls` and calls `gameStart`; no script jumps here |
| 19 / 20 | `gamewin` / `gameover` | show `levelscore` and `mscore`; button 473 (`btn0`) zeroes the scores and returns to frame 10 |

## Boot

The init actions sit on three frames (tag positions from the original): the nine class definitions
on frame 1, before the preloader `frame_1_DoAction_main`; the three `lib_*` registrations
(`lib_forward_wheel_main`, `lib_back_wheel_main`, `lib_man_main`) on frame 10; the game's own
`DoInitAction_main` on frame 11. Button 124 jumps from frame 10 to 15, button 147 from frames 11–12. Whether the player runs
frame 11's init action on that jump isn't settled here; S13's runtime check can answer it. The init
action declares the globals with their first values: `stopSoundFlag = false`,
`zastSoundFlag = true`, `life = 10`, `highQuality = true`, and `bikeSync`, `engine`, `objCamera`,
`back1`, `back2` all `null` until the first level is built.

## The level and the main loop

Frame 15 places the clip `mc_control` (sprite 33) with four clip actions: `onClipEvent(load)` calls
`initLevel`, `onClipEvent(enterFrame)` calls `processGame` (and starts `accSnd` on the up key), and two
`keyDown` handlers call `keyPressed`, which no script defines. Leaving `game` for `reset` and coming back
puts the clip on stage again, so its load handler runs `initLevel` once per attempt. That last step is
standard Flash timeline behaviour; the scripts don't state it.

- `initLevel` sends `mc_level` (sprite 387, labels `level1`…`level6`) to the current `level`, builds
  the physics objects once (`CBikeSynchronizer`, `CParticleEngine`, `CCamera`, two `CBack`), then
  each attempt: three `CParticle`s (back wheel, front wheel, body; mass 3), two wheels, three
  `CSpringConstraint`s, the hit map `mc_level.mc.mc_hit`, and `gameState = 0`.
- `processGame` runs every frame. While `gameState == 0` it adds the frame time to `timeCounter`,
  calls `showTime`, tilts the bike with the arrow keys (`CMan.LEFT_BUTTON` 37, `RIGHT_BUTTON` 39) along
  `calcBikeNVector`, steps `engine.process()`, `bikeSync.process()`, `objCamera.process()` and the two
  parallax layers, fires on the G and F keys (key codes 71, 70), brings the helicopter in when
  `helicounter` reaches 200, ends the level at `mc_finish`, and calls `loose` when the rider's head,
  body or leg point (`h`, `b`, `l`) hits the ground map.

`gameState` values, from their writers: 0 playing (`initLevel`, `resume`), 1 lost (`loose`), 2 level
complete (`processGame`), 3 game won (`processGame`), 4 paused (`pauseGame`).

## The physics

A Verlet particle system (`docs/gameplay-cparticleengine.md`): `CParticleEngine.process` measures the
time since the last call and runs up to `maxSteps` (2) fixed steps of `t` (0.02 s), each: forces
(gravity × mass), the wheels' added accelerations, `verlet`, the spring constraints, the wheel
collisions against the hit clip. `CWheel` samples 32 points on its rim against the hit map and pushes
itself out; `CBikeSynchronizer` places the bike, springs and rider clips from the three particles.

## The combat layer

The shots, the helicopter and the bombs live in clip actions on frame 15 and in `processGame`:
`fire`/`resetkfire` rate-limit the gun; shots are `bullet_id` or `rocket_id` clips named
`bullet_id<kval>` and listed in `_root.bulletArray`; `bullet_checker_mc` (sprite 455) tests them
against the boxes and the helicopter; the helicopter (`helicop`, sprite 446) drops `bomb`
(sprite 453), whose hits advance `health_mc` and call `loose` at its frame 4.

## Two layers of state

The scripts keep two of several things: `life` (10, decremented by `loose`) and `lifee` (5, decremented
by the crash clip, tested on frame 15); `level` (up to 10 in `nextLevel`) and `lvls` (1–15 on the
level selection; `gamewin` at 7); `scores` (shown in `mc_messageF`) and `mscore`/`tscore`/`levelscore`.
`processGame` also sets `stargeted = 5` just before testing `stargeted >= 3`, which makes that test always
true. A likely reading is that a bike-physics engine with Russian identifiers (`ugol`, `modul`,
`koeff…`, `mc_fon`) was re-skinned with a second layer of menus, combat and scoring. That reading is
unverified; nothing in the file names an author.

## Unknowns

`keyPressed` and `addLevelScores` are called but defined nowhere in the scripts. `rotates`,
`jeepselection` and `hell` are read and never written. No script jumps to `soundatta`, `main`,
`carselection` or `level selection`. The 19 functions of the init action are split by role across
`core.md`, `audio.md`, `ui.md`, `gameplay-bullet-id.md` and `gameplay-cbikesynchronizer.md`.

## Subsystems

- [audio](audio.md) — 6 function(s)
- [core](core.md) — 13 function(s)
- [gameplay/107](gameplay-107.md) — 2 function(s)
- [gameplay/112](gameplay-112.md) — 1 function(s)
- [gameplay/113](gameplay-113.md) — 1 function(s)
- [gameplay/150](gameplay-150.md) — 1 function(s)
- [gameplay/159](gameplay-159.md) — 1 function(s)
- [gameplay/197](gameplay-197.md) — 2 function(s)
- [gameplay/198](gameplay-198.md) — 1 function(s)
- [gameplay/205](gameplay-205.md) — 4 function(s)
- [gameplay/206](gameplay-206.md) — 2 function(s)
- [gameplay/218](gameplay-218.md) — 2 function(s)
- [gameplay/24](gameplay-24.md) — 1 function(s)
- [gameplay/358](gameplay-358.md) — 1 function(s)
- [gameplay/385](gameplay-385.md) — 2 function(s)
- [gameplay/399](gameplay-399.md) — 4 function(s)
- [gameplay/408](gameplay-408.md) — 4 function(s)
- [gameplay/415](gameplay-415.md) — 4 function(s)
- [gameplay/437](gameplay-437.md) — 1 function(s)
- [gameplay/440](gameplay-440.md) — 1 function(s)
- [gameplay/443](gameplay-443.md) — 4 function(s)
- [gameplay/446](gameplay-446.md) — 1 function(s)
- [gameplay/449](gameplay-449.md) — 1 function(s)
- [gameplay/453](gameplay-453.md) — 2 function(s)
- [gameplay/52](gameplay-52.md) — 2 function(s)
- [gameplay/86](gameplay-86.md) — 5 function(s)
- [gameplay/87](gameplay-87.md) — 1 function(s)
- [gameplay/97](gameplay-97.md) — 1 function(s)
- [gameplay/bullet_id](gameplay-bullet-id.md) — 4 function(s)
- [gameplay/cback](gameplay-cback.md) — 4 function(s)
- [gameplay/cbikesynchronizer](gameplay-cbikesynchronizer.md) — 6 function(s)
- [gameplay/ccamera](gameplay-ccamera.md) — 4 function(s)
- [gameplay/cman](gameplay-cman.md) — 12 function(s)
- [gameplay/cparticle](gameplay-cparticle.md) — 3 function(s)
- [gameplay/cparticleengine](gameplay-cparticleengine.md) — 15 function(s)
- [gameplay/cspringconstraint](gameplay-cspringconstraint.md) — 3 function(s)
- [gameplay/cvector2d](gameplay-cvector2d.md) — 20 function(s)
- [gameplay/cwheel](gameplay-cwheel.md) — 10 function(s)
- [gameplay/lib_man](gameplay-lib-man.md) — 1 function(s)
- [gameplay/rocket_id](gameplay-rocket-id.md) — 2 function(s)
- [gameplay/timeline-game](gameplay-timeline-game.md) — 10 function(s)
- [platform](platform.md) — 1 function(s)
- [ui](ui.md) — 36 function(s)

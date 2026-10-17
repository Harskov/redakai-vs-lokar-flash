# Formats

<!-- milestone M4's document: the save data, the level data and the asset formats as the matched code reads and writes them; a section with nothing to describe says so and why (`None: <the evidence>`) -->

## Save data

None: no script in the file saves or loads anything. The matched source and the reference listing of
all 95 scripts contain no `SharedObject`, `LoadVars`, `loadVariables`, `XML`, `loadMovie`, `fscommand` or
`LocalConnection`. Scores, lives and the reached level (`lvls`, `level`, `life`, `lifee`, `tscore`,
`mscore`, `levelscore`) are timeline variables that last only while the movie runs. The only calls
that leave the movie are the two `getURL` buttons (`DefineButton2_127`, `DefineButton2_389`), which
open the game's web site in a new window.

## Level data

A level is not a data file. It is a frame of the clip `mc_level` (sprite 387, 6 frames,
`assets/MANIFEST.json`), which is placed on the main timeline's frame 15 `game`. The code reaches a
level only through instance names:

| Instance (under `mc_level`) | What reads it | Role |
|---|---|---|
| `gotoAndStop(level)` | `initLevel` (reference) | picks the level: frame number `level` |
| `mc.mc_hit` | `initLevel` hides it, `CParticleEngine.setHitMovie` keeps it, `CWheel.checkCollision` (reference) and `processGame` test it with `hitTest(x, y, true)` | the ground: a shape hit-tested point by point, never drawn |
| `mc.mc_bike` | `initLevel`, `processGame` | the bike's start position and the parent of its parts |
| `mc.mc_finish` | `processGame` | the finish line: the level ends when the bike passes its `_x` (190 px earlier on one of the two tests) |
| `mc.mc_fon.mc_grass.mc1`/`mc2`, `mc.mc_fon.mc_hill.mc1`/`mc2` | `initLevel` → `CBack.init`; `processGame` → `CBack.process` | two parallax layers, each a pair of tiles |
| `mc.s1` … `mc.s20` | `processGame` (s1–s20, hit once each, marked `bikehit`); `initLevel` (s1–s10, sent to a random frame 1–3) | clips placed along the track; what they show is not known |
| `mc_minimap.mc_stage`, `mc_minimap.s<n>` | `initLevel` (reference) | the level map: stage frame `level`, earlier levels at frame 2, the current one at frame 3 |

Which level is played comes from two counters. `level` (the frame of `mc_level`) is set from `lvls`
by `frame_15_DoAction_main` for `lvls` 1–15, and `nextLevel` increments it up to 10. Sprite 387 has
6 frames, so the scripts do not settle what the player shows for `level` 7–10. The behaviour
checkpoints inject no input, so they do not answer it either.

## Asset formats

The scripts reach library assets by export name (the 22 `ExportAssets` entries, `DOSSIER.md`; each is
the `name` of its asset in `assets/MANIFEST.json`):

- sounds: `playSnd` (matched) attaches a sound to a `Sound` on its timeline and starts it;
  `frame_10_DoAction_main` (reference) creates `intro` from `bat_sound`, `accSnd`, `accLoop`, `pb` from
  `play bg1` and `cra` from `crashbike`. No export is named `play bg1`, `crashbike` or `lib_snd_fail` (the
  sound `loose` passes to `playSnd`), so the scripts ask for three sounds the manifest does not export.
  All 10 sounds are MP3 (11–44 kHz, mono).
- clips made at run time: `processGame` (matched) attaches `bullet_id` (sprite 20) and `rocket_id`
  (sprite 12) as `bullet_id<kval>` at `getNextHighestDepth()`.
- clips bound to classes: `lib_forward_wheel` and `lib_back_wheel` (sprites 115, 116) to `CWheel`, and
  `lib_man` (sprite 95) to `CMan`, by `Object.registerClass` in their init actions (matched).
- everything else (shapes, images, text, fonts, the empty video stream 53) is placed on timelines and
  is reached only by instance name, never by a script that loads or decodes it.

The tag formats, from the manifest:

- button, DefineButton2: 8 (`assets/MANIFEST.json`)
- edit-text, DefineEditText: 7 (`assets/MANIFEST.json`)
- font, DefineFont3: 11 (`assets/MANIFEST.json`)
- font-align, DefineFontAlignZones: 11 (`assets/MANIFEST.json`)
- image, jpeg+alpha (DefineBitsJPEG3): 14 (`assets/MANIFEST.json`)
- image, lossless+alpha (DefineBitsLossless2): 1 (`assets/MANIFEST.json`)
- morph-shape, DefineMorphShape: 19 (`assets/MANIFEST.json`)
- morph-shape, DefineMorphShape2: 1 (`assets/MANIFEST.json`)
- shape, DefineShape: 98 (`assets/MANIFEST.json`)
- shape, DefineShape2: 26 (`assets/MANIFEST.json`)
- shape, DefineShape3: 10 (`assets/MANIFEST.json`)
- shape, DefineShape4: 29 (`assets/MANIFEST.json`)
- sound, MP3: 10 (`assets/MANIFEST.json`)
- sprite, DefineSprite: 206 (`assets/MANIFEST.json`)
- text, DefineText: 59 (`assets/MANIFEST.json`)
- video, DefineVideoStream: 1 (`assets/MANIFEST.json`)

## Evidence

- a search of `src/` and of the reference listing for the save and load calls named above finds none
  (the two `getURL` buttons are the only calls that leave the movie)
- `initLevel` (reference listing, `DoInitAction`): `mc_level.gotoAndStop(level)`, `mc_level.mc.mc_hit._visible = false`,
  `engine.setHitMovie(mc_level.mc.mc_hit)`, the `CBack.init` calls on `mc_fon.mc_grass` and `mc_fon.mc_hill`
- `processGame` (matched): `mc_level.mc.mc_hit.hitTest(x, y, true)` for the rider's `h`, `b` and `l` points;
  the two `mc_finish._x` tests; the `s1`…`s20` hit test; `attachMovie("bullet_id" | "rocket_id", …)`
- `CWheel.checkCollision` and `CWheel.pushOut` (reference listing): `hit_mc.hitTest(x, y, true)`
- `assets/MANIFEST.json`: sprite 387 with 6 frames; 22 named assets, matching the 22 `ExportAssets` entries in
  `DOSSIER.md`; no asset named `play bg1`, `crashbike` or `lib_snd_fail`; 10 MP3 sounds, all mono
- `lib_forward_wheel_main`, `lib_back_wheel_main`, `lib_man_main` (matched): the three `Object.registerClass` calls

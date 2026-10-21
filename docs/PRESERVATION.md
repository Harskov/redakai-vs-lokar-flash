# Preservation record — Redakai vs Lokar

## Provenance

The original is the user's own copy, `Redakai vs Lokar.swf` (1542563 bytes), read from `<mirror>/Redakai vs Lokar.swf` at S1 on 2026-10-14.
sha1 `1395899485f5b41da5b94ba05401d22ea1810ae0`, sha256 `ced1985307d9ac4add72f8fb4dd23729428691075d7c0b2f9ffeefd72700a508`. The file itself is never committed; `config/target.json` carries the hashes.

## Container

CWS SWF version 9, 700x500 px at 35 fps, 20 frames on the main
timeline, 857 top-level tags, 95 scripts (AVM1).

## Reference exports

FFDec (JPEXS Free Flash Decompiler v.26.3.0) P-code and ActionScript exports under `reference/` (gitignored) with `reference/MANIFEST.json`
committed (counts and hashes). Assets are inventoried in `assets/MANIFEST.json` at S7 without their content.

## The rebuild

Every one of the 95 scripts is compiled from `src/` and compared with the original under the pinned criterion,
normalized P-code equality (`build/check.json`). The compiler is FFDec 26.3.0 with one patch,
`tools/ffdec-26.3.0-define-kind-1.patch`: the original compiler's choice of function header (`DefineFunction` for a
body that calls `eval` or `set`; `DefineFunction2` for a parameter, a register local, a preloadable identifier or an
enclosing function; `DefineFunction` otherwise), which reproduces the header of every function the original defines.
`configure.py` downloads FFDec's release and the one source file the patch changes, applies the patch and builds that
class; a Java agent loads it beside the unmodified jar, so a clean clone builds what the workbench builds.

## Runtime notes

Filled at S13 from the behaviour checks (Ruffle renders of the original and the rebuilt file at the recorded checkpoints).

- 2026-10-16, Ruffle's exporter built from the pinned 0.7.1 commit, headless on Mesa's software Vulkan: all 32
  checkpoints in `tests/behaviour/checkpoints.json` (the first frame, the tick at which each of the 11 main-timeline
  labels' frames would start, every 35th tick to 20 s) render pixel-identical for the original and the rebuilt file
  (`tests/behaviour/hashes.json`); re-checked the same day against the rebuilt tree, again 32 of 32 identical.
- 2026-10-17, re-checked with 179 of 202 functions matched (81 of 95 scripts rebuilt from source): 32 of 32
  identical, every render byte-identical to the previous check's.
- 2026-10-21, re-checked with 200 of 202 functions matched (94 of 95 scripts rebuilt from source): 32 of 32
  identical, every render byte-identical to the previous check's; re-checked the same day after three sources were
  rewritten without their `!FAKE` markers, again 32 of 32 identical and the renders unchanged.
- 2026-10-21, re-checked with 202 of 202 functions matched (95 of 95 scripts rebuilt from source) and an input timeline:
  Ruffle's exporter built from the pinned commit with the project's patch, which runs one session of a file from scripted
  input (mouse moves, presses and releases at stage pixels, keys, the player's context-menu items, per tick), with
  `getTimer` and the timers on a virtual clock advanced by 1000/35 ms a tick and `Math.random` seeded from a fixed clock.
  One session of each file, 83 checkpoints (the 32 unattended ones, which all fall before the first input at tick 705,
  then 51 along the timeline): 83 of 83 pixel-identical; two runs of the session give the same bytes.
- What the renders show. Without input (the first 32 checkpoints): the loader on the first frame, then the title menu
  (Start Game and More Games beside the control instructions) on every other checkpoint, its background animated;
  playback stops there, so a label's checkpoint shows the menu, not the frame the label names. Along the timeline: the
  menu frames 11 and 12 with the start and help buttons' hover animations; frame 13 `carselection` and frame 14 `help`,
  each an unfinished panel; level 1 ridden with Up held, a missile (F) and compact rockets (G) fired, the speaker toggled
  off and on, the enemy attacking, crashes ("R.I.P!!") and replays taking a life each until game over ("You lost him");
  Play Again back to the logo frame and a new game; the completion screen ("Well played!! But Lokar got away") and its
  Pursue Him button into level 2; the level-selection panel (frame 18, most of it right of the stage); the gamewin
  screen ("You saved the world"); and a game started from each level button, le10 down to le1 (levels 7 to 10 read
  "Level n/6": the game defines six).
- Coverage: in the rebuilt file's session 25 of the 30 matched input handlers run, each listed with the tick it first
  ran in `tests/behaviour/last-compare.json`: the buttons' releases, rollOvers and rollOuts, the speaker's two presses,
  the two key handlers of the game frame and frame 18's level buttons le1 to le10. The five that do not run, frame 18's
  `onRelease_11` to `onRelease_15`, are assigned to the clips `le11` to `le15`, which the movie never places (frame 18
  places `le1` to `le10` only), so no input reaches them in the original either. Frames 13 and 18 are reached with the
  Flash Player's own context menu (Forward and Back), which the game leaves on: no code of the game goes there. `le5` and
  `le10` lie right of the 700-pixel stage and are clicked there.

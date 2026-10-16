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

## Runtime notes

Filled at S13 from the behaviour checks (Ruffle renders of the original and the rebuilt file at the recorded checkpoints).

- 2026-10-16, Ruffle's exporter built from the pinned 0.7.1 commit, headless on Mesa's software Vulkan: all 32
  checkpoints in `tests/behaviour/checkpoints.json` (the first frame, the tick at which each of the 11 main-timeline
  labels' frames would start, every 35th tick to 20 s) render pixel-identical for the original and the rebuilt file
  (`tests/behaviour/hashes.json`); re-checked the same day against the rebuilt tree, again 32 of 32 identical.
- What the renders show: two states only. The first frame shows the loader ("Loading Game" and its bar); every other
  checkpoint shows the title menu (the Start Game and More Games buttons beside the control instructions), its animated
  background differing from checkpoint to checkpoint. Playback stops on the menu, so a label's checkpoint (`carselection`,
  `game`, `gameover` and the rest) shows the menu, not the frame the label names.
- Coverage: the exporter plays the file from its first frame with no mouse or keyboard input, so every checkpoint shows
  the unattended playback path; the 28 matched input handlers run in no checkpoint, and car selection, the levels,
  winning and losing are not exercised.

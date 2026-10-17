# audio

Music and sound effects. The music is two looping clips, `mc_sloop` and `mc_sloop_zast`, switched by frame (2 playing, 3 silent) and gated by `stopSoundFlag`; `zastSoundFlag` picks which one plays (true on the menus through `newGame`, false in play through `gameStart`). The effects are `Sound` objects made on frames 10 and 15.

## Functions

- `updateSoundLoop` (matched) — unless muted (stopSoundFlag), plays the music loop zastSoundFlag selects (mc_sloop_zast or mc_sloop, frame 2) and parks the other on frame 3; called by gameStart and newGame
- `soundOff` (matched) — mutes the music: the loop in use goes to frame 3 and stopSoundFlag is set; no script calls it
- `soundOn` (matched) — unmutes the music: the loop in use goes back to frame 2 and stopSoundFlag is cleared; no script calls it
- `playSnd` (matched) — plays a library sound once by its linkage name from a new Sound on this timeline; loose plays lib_snd_fail, a name the file does not export
- `frame_10_DoAction_main` (not yet matched) — the logo frame: Sound objects intro (bat_sound, looped), accSnd, accLoop, pb (play bg1), cra (crashbike); scorecard, scorecard2, levelscore 0, lifee 5
- `frame_15_DoAction_main` (not yet matched) — the game frame: defines firebomb and setBright, restarts intro, loops btnon at volume 5, maps lvls to level, gameover when lifee is 0

## Not known

- `soundOn` and `soundOff` have no caller in the scripts.
- `lib_snd_fail`, `play bg1` and `crashbike` are not among the file's 22 export names, so those `attachSound` calls may attach nothing; S13's runtime check can settle it.
- `zast` may be Russian for a title screen (заставка); a reading, not evidence.

## Evidence

- export names `bat_sound`, `accSnd`, `accLoop`, `btnon`, `intro`, `helicop_snd` (the original's ExportAssets)
- `mc_sloop.gotoAndStop(2|3)` in `updateSoundLoop`, `soundOn`, `soundOff`, `initLevel`, `resume`, `pauseGame`, `loose`, `processGame`
- `attachSound` calls in `frame_10_DoAction_main`, `frame_15_DoAction_main`, `playSnd`

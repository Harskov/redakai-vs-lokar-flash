# audio

Music and sound effects. The music is two looping clips, `mc_sloop` and `mc_sloop_zast`, switched by frame (2 playing, 3 silent) and gated by `stopSoundFlag`; `zastSoundFlag` picks which one plays (true on the menus through `newGame`, false in play through `gameStart`). The effects are `Sound` objects made on frames 10 and 15.

## Functions

- `updateSoundLoop` (not yet matched) — unless stopSoundFlag: plays the loop zastSoundFlag selects and silences the other
- `soundOff` (not yet matched) — silences the active loop and sets stopSoundFlag
- `soundOn` (not yet matched) — plays the active loop and clears stopSoundFlag
- `playSnd` (not yet matched) — plays a library sound once from a new Sound on this clip (loose plays lib_snd_fail)
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

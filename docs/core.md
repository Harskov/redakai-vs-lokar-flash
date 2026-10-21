# core

The game's control functions: the init action of sprite 150 (`DoInitAction`, frame 11) and the preloader on frame 1. They write `gameState` and move the main timeline between `main`, `reset`, `game` and `comple`. The frame-by-frame flow and the main loop are in `ARCHITECTURE.md`.

## Functions

- `DoInitAction_main` (matched) — the init action's own statements: declares the game's globals with their first values (stopSoundFlag false, zastSoundFlag true, highQuality true, life 10; bikeSync, engine, objCamera, back1, back2 null)
- `gameStart` (matched) — a new run: scores, timeCounter and stargeted 0, life 10, the in-game music (zastSoundFlag cleared), level 0, then nextLevel to enter level 1; called by the level buttons and button 461
- `nextLevel` (matched) — the next level: stargeted and levelTimeCounter cleared, level++ and the timeline stepped through reset back to game; at level 10 it calls newGame instead
- `replay` (matched) — restarts the current level: clears stargeted and steps the timeline through reset back to game; called by the crash clip
- `newGame` (matched) — back to the main frame with stargeted cleared and the menu music (zastSoundFlag set)
- `initLevel` (matched) — builds one attempt at the current level, called by mc_control's load: the minimap's marks, `mc_level` at frame `level`, the bike's three particles with two wheels and three springs, the camera and hit clip, the sound loop unless muted, gameState 0, and the level clip's `s1` to `s10` each sent to a random frame 1 to 3; the physics objects are created on the first call and the engine cleared on later ones. Its header is the original compiler's `DefineFunction2` for a body with register locals and no parameter (`ARCHITECTURE.md`, the source and its compiler)
- `processGame` (matched) — the per-frame step while gameState is 0, called by mc_control's enterFrame: clock, up-key gas, arrow-key tilt, physics, camera, parallax, pickups s1-s20, shots on G and F, the helicopter at helicounter 200, the finish line and the rider's ground tests
- `resume` (matched) — undoes pauseGame: the music back unless muted, the message clip cleared to empty, the rider's animation restarted, gameState 0; no script calls it
- `pauseGame` (matched) — pauses: the pause message, the music stopped unless muted, the rider's animation frozen, gameState 4; no script calls it
- `clearStuff` (matched) — clears the attempt's moving parts: every shot in bulletArray hidden, sent to 39 and removed, the list emptied, the bomb and helicopter back to their start, both brightnesses reset; called by loose and processGame's finish
- `loose` (matched) — a lost attempt (the author's spelling of lose): clearStuff, tscore into mscore and txtscore, the fail sound, life--, the wheels moved 1000 px right, the jeep parts and the crash clip played, the times and score shown, gameState 1
- `frame_1_DoAction_main` (matched) — the preloader frame: holds, empties the bar (preloader width 0), shows bar and background, and installs the bar's per-frame handler
- `frame_1_DoAction.onEnterFrame` (matched) — the preloader bar: width and text follow the percent loaded (getBytesLoaded over getBytesTotal); at 100% it hides both, removes itself and plays from frame 10

## Not known

- `loose` decrements `life`; the crash clip decrements `lifee`, and only `lifee` is tested (frame 15). No script reads `life` otherwise.
- `processGame` calls `addLevelScores`, which no script defines.

## Evidence

- `gameState` writers in the reference listing: `initLevel` and `resume` (0), `loose` (1), `processGame` (2, 3), `pauseGame` (4)
- the frame labels `main`, `reset`, `game`, `comple` (DOSSIER.md) named by `newGame`, `nextLevel`, `replay`, `processGame`
- `Math.floor(Math.random() * 3 + 1)` for `mc_level.mc["s" + i]`, i 1 to 10, in `initLevel`
- `mc_control` (sprite 33, root frame 15) calls `initLevel` on load and `processGame` on enterFrame (gameplay-timeline-game.md)
- DoInitAction tag 304 belongs to sprite 150 and sits on root frame 11 (the original's tag order)

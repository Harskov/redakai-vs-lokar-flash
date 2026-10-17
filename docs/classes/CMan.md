# CMan

The rider on the bike: a MovieClip class (`Object.registerClass("lib_man", CMan)`) whose instance is reached as `bikeSync.mc_bike.mc.mc_body_man.mc`. It leans left or right with the arrow keys and plays its lean animation in its inner clip `mc`.

**Prototype.** `class CMan extends MovieClip`; fields `mc`, `state`, `stopFlag`; statics `LEFT_BUTTON = 37`, `RIGHT_BUTTON = 39` (the arrow key codes), `ANIM_FRAMES = 7`.

**Fields.** `stopFlag`: cleared by the constructor and `startAnim`, set by `stopAnim`; `onEnterFrame` does nothing while it is set. `state`: 0 at construction; `onEnterFrame`, `toLeft`, `toRight`, `fromLeft`, `fromRight` move it through 0-6 (the lean states; their meanings are not yet read). `mc`: the inner animation clip, stopped by `stopMCAnim`.

| Method | Accepted | Callers (confirmed in the scripts) |
|---|---|---|
| `CMan()` | yes | the player, when `lib_man` is placed (registerClass) |
| `stopMCAnim()` | yes | processGame, loose (after `stopAnim`) |
| `stopAnim()` | yes | processGame, pauseGame, loose |
| `startAnim()` | yes | resume |
| `onEnterFrame`, `toLeft`, `toRight`, `fromLeft`, `fromRight`, `endMove` | yes | the player each frame; each other |

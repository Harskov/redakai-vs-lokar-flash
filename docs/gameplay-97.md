# gameplay/97

The bike body's inner clip: sprite 97 is `mc` inside `lib_bike_body` (sprite 98). It holds the jeep, the rider (`mc_body_man`) and the wheel marks `CBikeSynchronizer` reads; its frame action dresses the jeep for the selected vehicle.

## Functions

- `DefineSprite_97_frame_1_DoAction_main` (not yet matched) — sets `jeep` to the frame _root.jeepselection names

## Not known

- `jeepselection` has no writer in the scripts

## Evidence

- placements `mc` in 98, and `jeep`, `mc_body_man`, `mc_f_point`, `mc_s_wheel_back` inside 97 (the original's PlaceObject tags)
- `mc_bike.mc.mc_s_wheel_back` and `mc_bike.mc.mc_f_point` in `CBikeSynchronizer.init` and `setParticles`

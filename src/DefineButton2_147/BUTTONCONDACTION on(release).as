// on frames 11-12 beside the help button: play the game frame (15) from level 1;
// unlike btn1 on the logo frame, it leaves tscore and mscore as they are
on(release){
   gotoAndPlay(15);
   _root.lvls = 1;
}

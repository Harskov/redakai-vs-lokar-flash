// the reset button: wipe the round's scores, restart the level
on(release){
   _root.tscore = 0;
   _root.mscore = 0;
   gotoAndPlay(15);
   _root.lvls = 1;
}

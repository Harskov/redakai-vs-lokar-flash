// btn1 on the logo frame: zero both scores and play the game frame (15) from level 1
on(release){
   _root.tscore = 0;
   _root.mscore = 0;
   gotoAndPlay(15);
   _root.lvls = 1;
}

// btn0 on the gamewin and gameover frames: zero both scores and send the main
// timeline back to the logo frame (10)
on(release){
   _root.tscore = 0;
   _root.mscore = 0;
   _root.gotoAndStop(10);
}

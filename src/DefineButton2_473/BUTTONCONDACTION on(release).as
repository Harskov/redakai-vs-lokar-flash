// the round-reset button: clear both scores, back to frame 10
on(release){
   _root.tscore = 0;
   _root.mscore = 0;
   _root.gotoAndStop(10);
}

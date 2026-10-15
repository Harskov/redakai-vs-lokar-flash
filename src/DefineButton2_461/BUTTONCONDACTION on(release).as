// btn2 on the comple frame: the score so far carries over into tscore, then gameStart
// begins the next level (frame 17 has already raised lvls)
on(release){
   _root.tscore = _root.mscore;
   gameStart();
}

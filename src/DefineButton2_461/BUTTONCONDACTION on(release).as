// the release handler: copy the match score into the total, then start the game
on(release){
   _root.tscore = _root.mscore;
   gameStart();
}

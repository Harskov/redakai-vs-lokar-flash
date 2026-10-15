// sprite 52 plays while _root.bexplode is set: frame 15's hit check sets it when the
// bike takes a hit, and sprite 52's frame 2 clears it
onClipEvent(enterFrame){
   if(_root.bexplode == true)
   {
      this.play();
   }
}

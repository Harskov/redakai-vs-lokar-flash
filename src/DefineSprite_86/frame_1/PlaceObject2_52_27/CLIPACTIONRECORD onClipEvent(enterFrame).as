// plays this clip's timeline once _root.bexplode is set (probably an explosion trigger from the main timeline)
onClipEvent(enterFrame){
   if(_root.bexplode == true)
   {
      this.play();
   }
}

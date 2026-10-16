// every frame the parent runs processGame; while key 38 (the up arrow) is held, accSnd
// starts once per press, _accSnd ("yes"/"no") remembering that it already did
onClipEvent(enterFrame){
   this._parent.processGame();
   if(Key.isDown(38))
   {
      if(_root._accSnd == "no")
      {
         _root.accSnd.start(0, 1);
         _root._accSnd = "yes";
      }
   }
   else
   {
      _root._accSnd = "no";
   }
}

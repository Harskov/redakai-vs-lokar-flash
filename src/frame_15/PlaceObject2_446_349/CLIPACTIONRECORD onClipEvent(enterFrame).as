// the helicopter clip: while heliactivate is set and it is not shot down it flies left until
// x -270 ends the pass; once helidestroy is set it falls, dimmed, and below y 600 it is reset
// to its start, firebomb is called and the hell sound plays
onClipEvent(enterFrame){
   if(_root.heliactivate == true && _root.helidestroy != true)
   {
      this._x -= 4;
      if(this._x < -270)
      {
         _root.heliactivate = false;
         _root.helicounter = 0;
      }
   }
   if(_root.helidestroy == true)
   {
      this.gotoAndStop(1);
      this._rotation = -20;
      this._y += 12;
      _root.setBright(_root.helicop, -150);
      _root.bomb._alpha = 0;
      if(this._y > 600)
      {
         this._rotation = 0;
         this._y = 58.4;
         this._x = 1006.4;
         _root.setBright(_root.helicop, 0);
         _root.helidestroy = false;
         _root.firebomb();
         _root.hell.start(0, 99);
      }
   }
}

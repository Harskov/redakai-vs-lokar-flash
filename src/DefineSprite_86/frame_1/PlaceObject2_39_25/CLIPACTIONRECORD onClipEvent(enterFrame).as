// the muzzle marker's stage position, each frame, as (mx3, my3): where processGame
// puts a new shot
onClipEvent(enterFrame){
   var point3 = {x:this._x, y:this._y};
   this.localToGlobal(point3);
   _root.mx3 = point3.x;
   _root.my3 = point3.y;
}

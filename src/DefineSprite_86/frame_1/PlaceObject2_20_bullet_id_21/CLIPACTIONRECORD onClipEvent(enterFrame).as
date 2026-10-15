// bullet_mc's stage position, each frame, as (mx2, my2): processGame aims from
// (mx1, my1) towards it
onClipEvent(enterFrame){
   var point = {x:this._x,y:this._y};
   this.localToGlobal(point);
   _root.mx2 = point.x;
   _root.my2 = point.y;
}

// the bullet's position on the stage, published every frame for the hit test
onClipEvent(enterFrame){
   var point = {x:this._x,y:this._y};
   this.localToGlobal(point);
   _root.mx2 = point.x;
   _root.my2 = point.y;
}

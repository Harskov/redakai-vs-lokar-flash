// publish this clip's position on the main timeline as _root.mx3/_root.my3
onClipEvent(enterFrame){
   var point3 = {x:this._x, y:this._y};
   this.localToGlobal(point3);
   _root.mx3 = point3.x;
   _root.my3 = point3.y;
}

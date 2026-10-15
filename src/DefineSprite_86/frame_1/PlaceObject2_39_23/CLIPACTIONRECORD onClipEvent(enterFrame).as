// the first aim marker's stage position, each frame, as (mx1, my1): where
// processGame's aim line starts
onClipEvent(enterFrame)
{
   var point2 = {x:this._x, y:this._y};
   this.localToGlobal(point2);
   _root.mx1 = point2.x;
   _root.my1 = point2.y;
}

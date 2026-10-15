// tracks this clip's position on the stage each frame: localToGlobal into _root.mx1/my1
onClipEvent(enterFrame)
{
   var point2 = {x:this._x, y:this._y};
   this.localToGlobal(point2);
   _root.mx1 = point2.x;
   _root.my1 = point2.y;
}

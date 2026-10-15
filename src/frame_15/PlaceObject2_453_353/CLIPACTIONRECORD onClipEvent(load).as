// the clip starts turned to 220 degrees; despite its name, the degrees field holds that angle in radians (pi / 180)
onClipEvent(load){
   this._rotation = 220;
   this.degrees = this._rotation * 0.01745329;
}

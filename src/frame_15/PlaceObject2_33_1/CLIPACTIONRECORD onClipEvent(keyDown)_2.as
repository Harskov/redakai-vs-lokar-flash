// the key handler lives on the clip but the press is handled one level up, then the display is refreshed
onClipEvent(keyDown){
   this._parent.keyPressed();
   updateAfterEvent();
}

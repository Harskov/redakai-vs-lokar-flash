// picks one of five background frames at random, but no clip in this sprite
// is named bg, so the call does nothing and the backdrop stays as placed
var bgss = 1 + random(5);
bg.gotoAndStop(bgss);

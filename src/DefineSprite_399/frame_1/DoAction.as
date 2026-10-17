// the switch's first frame: hold, and point btnon's press to the frame labelled `off`;
// probably the sound switch, since the `off` frame stops every sound
stop();
// the press while on: play from the frame labelled "off"
btnon.onPress = function()
{
   gotoAndPlay("off");
};

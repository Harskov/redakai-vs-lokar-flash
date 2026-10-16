// the switch's `off` frame: hold, stop every sound, and point btnon's press back to `on`;
// probably the sound switch
stop();
stopAllSounds();
// the press while off: play from the frame labelled "on"
btnon.onPress = function()
{
   gotoAndPlay("on");
};

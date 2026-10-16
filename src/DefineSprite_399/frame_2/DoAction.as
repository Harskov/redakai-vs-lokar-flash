// the sound button: stop the clip's timeline and all sounds; the press itself is the onPress record
stop();
stopAllSounds();
btnon.onPress = function()
{
   gotoAndPlay("on");
};

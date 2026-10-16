// the press handler: play from the frame labelled "off"
stop();
// the press while on: play from the frame labelled "off"
btnon.onPress = function()
{
   gotoAndPlay("off");
};

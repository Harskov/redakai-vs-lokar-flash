// the frame after a level: count the level and add 100 to scorecard; frame 16 removed every text
// field, so the two writes show nothing and levelscore reads back undefined; once lvls reaches 7
// go to the gamewin frame
stop();
stopAllSounds();
lvls++;
_root.scorecard = Number(_root.scorecard) + Number(100);
txtlevel.text = _root.scorecard;
txtscore.text = Number(_root.levelscore) + Number(_root.scorecard);
_root.levelscore = txtscore.text;
if(_root.lvls == 7)
{
   gotoAndStop("gamewin");
}

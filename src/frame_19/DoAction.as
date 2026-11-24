// the gamewin frame (19): hold, stop every sound and show the score in txtscore2; no field is
// named txtfinalscore, so the levelscore line shows nothing
stop();
stopAllSounds();
txtfinalscore.text = _root.levelscore;
txtscore2.text = _root.mscore + " points";

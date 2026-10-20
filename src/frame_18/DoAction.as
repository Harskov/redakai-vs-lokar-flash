// the level screen's start-up: silence the timeline and install the enter-frame handler that drives it
stop();
stopAllSounds();
// every frame: each level button up to lvls (le1 to le15) shows its second frame and, released, starts a game at its level
onEnterFrame = function()
{
   if(_root.lvls >= 1)
   {
      _root.le1.gotoAndStop(2);
      // le1, enabled once lvls reaches 1: a new game at level 1 (frame 15 builds the level from lvls)
      _root.le1.onRelease = function()
      {
         _root.lvls = 1;
         gameStart();
      };
   }
   if(_root.lvls >= 2)
   {
      _root.le2.gotoAndStop(2);
      // le2, enabled once lvls reaches 2: a new game at level 2 (frame 15 builds the level from lvls)
      _root.le2.onRelease = function()
      {
         _root.lvls = 2;
         gameStart();
      };
   }
   if(_root.lvls >= 3)
   {
      _root.le3.gotoAndStop(2);
      // le3, enabled once lvls reaches 3: a new game at level 3 (frame 15 builds the level from lvls)
      _root.le3.onRelease = function()
      {
         _root.lvls = 3;
         gameStart();
      };
   }
   if(_root.lvls >= 4)
   {
      _root.le4.gotoAndStop(2);
      // le4, enabled once lvls reaches 4: a new game at level 4 (frame 15 builds the level from lvls)
      _root.le4.onRelease = function()
      {
         _root.lvls = 4;
         gameStart();
      };
   }
   if(_root.lvls >= 5)
   {
      _root.le5.gotoAndStop(2);
      // le5, enabled once lvls reaches 5: a new game at level 5 (frame 15 builds the level from lvls)
      _root.le5.onRelease = function()
      {
         _root.lvls = 5;
         gameStart();
      };
   }
   if(_root.lvls >= 6)
   {
      _root.le6.gotoAndStop(2);
      // le6, enabled once lvls reaches 6: a new game at level 6 (frame 15 builds the level from lvls)
      _root.le6.onRelease = function()
      {
         _root.lvls = 6;
         gameStart();
      };
   }
   if(_root.lvls >= 7)
   {
      _root.le7.gotoAndStop(2);
      // le7, enabled once lvls reaches 7: a new game at level 7 (frame 15 builds the level from lvls)
      _root.le7.onRelease = function()
      {
         _root.lvls = 7;
         gameStart();
      };
   }
   if(_root.lvls >= 8)
   {
      _root.le8.gotoAndStop(2);
      // le8, enabled once lvls reaches 8: a new game at level 8 (frame 15 builds the level from lvls)
      _root.le8.onRelease = function()
      {
         _root.lvls = 8;
         gameStart();
      };
   }
   if(_root.lvls >= 9)
   {
      _root.le9.gotoAndStop(2);
      // le9, enabled once lvls reaches 9: a new game at level 9 (frame 15 builds the level from lvls)
      _root.le9.onRelease = function()
      {
         _root.lvls = 9;
         gameStart();
      };
   }
   if(_root.lvls >= 10)
   {
      _root.le10.gotoAndStop(2);
      // le10, enabled once lvls reaches 10: a new game at level 10 (frame 15 builds the level from lvls)
      _root.le10.onRelease = function()
      {
         _root.lvls = 10;
         gameStart();
      };
   }
   if(_root.lvls >= 11)
   {
      _root.le11.gotoAndStop(2);
      // le11, enabled once lvls reaches 11: a new game at level 11 (frame 15 builds the level from lvls)
      _root.le11.onRelease = function()
      {
         _root.lvls = 11;
         gameStart();
      };
   }
   if(_root.lvls >= 12)
   {
      _root.le12.gotoAndStop(2);
      // le12, enabled once lvls reaches 12: a new game at level 12 (frame 15 builds the level from lvls)
      _root.le12.onRelease = function()
      {
         _root.lvls = 12;
         gameStart();
      };
   }
   if(_root.lvls >= 13)
   {
      _root.le13.gotoAndStop(2);
      // le13, enabled once lvls reaches 13: a new game at level 13 (frame 15 builds the level from lvls)
      _root.le13.onRelease = function()
      {
         _root.lvls = 13;
         gameStart();
      };
   }
   if(_root.lvls >= 14)
   {
      _root.le14.gotoAndStop(2);
      // le14, enabled once lvls reaches 14: a new game at level 14 (frame 15 builds the level from lvls)
      _root.le14.onRelease = function()
      {
         _root.lvls = 14;
         gameStart();
      };
   }
   if(_root.lvls >= 15)
   {
      _root.le15.gotoAndStop(2);
      // le15, enabled once lvls reaches 15: a new game at level 15 (frame 15 builds the level from lvls)
      _root.le15.onRelease = function()
      {
         _root.lvls = 15;
         gameStart();
      };
   }
};

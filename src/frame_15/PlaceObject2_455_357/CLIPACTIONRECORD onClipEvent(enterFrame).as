// bullet hits while bulletArray holds any and arrdeactivate is unset: a shown bullet left of x 710 that hits
// box 1-7 of mc_level still on frame 1 plays it and its masks (a "bullet" only, 10 points), else one hitting the
// level helicopter left of x 650 brightens it, and 6 hits or a rocket explode it (50); a hidden or far bullet is cleared
onClipEvent(enterFrame){
   var blen = _root.bulletArray.length;
   if(blen > 0 && _root.arrdeactivate != true)
   {
      i = 0;
      while(i < blen)
      {
         // !FAKE: the author wrote if(_root.bulletArray[i] != ""); the doubled parentheses keep the double Not before the branch
         if((_root.bulletArray[i] != ""))
         {
            if(eval("_root." + _root.bulletArray[i])._alpha == 100 && eval("_root." + _root.bulletArray[i])._x < 710)
            {
               pi = 1;
               while(pi < 8)
               {
                  tmpMov = eval("_root.mc_level.mc.box" + pi);
                  if(tmpMov._currentframe == 1)
                  {
                     if(eval("_root." + _root.bulletArray[i]).hitTest(tmpMov) == true && eval("_root." + _root.bulletArray[i]).weapontype == "bullet")
                     {
                        eval("_root." + _root.bulletArray[i])._alpha = 0;
                        eval("_root." + _root.bulletArray[i]).gotoAndStop(39);
                        tmpMov.play();
                        eval("_root.mc_level.mc.mask_mc.box" + pi).play();
                        eval("_root.mc_level.mc.mc_hit.mask_hit_mc.box" + pi).play();
                        _root.mscore += 10;
                        _root.txtscore.text = _root.mscore;
                        _root.score_mc.gotoAndPlay(2);
                     }
                  }
                  else if(eval("_root." + _root.bulletArray[i]).hitTest(_root.helicop) == true && _root.helicop._rotation == 0 && _root.helicop._x < 650)
                  {
                     eval("_root." + _root.bulletArray[i])._alpha = 0;
                     eval("_root." + _root.bulletArray[i]).gotoAndStop(39);
                     _root.helicop.play();
                     _root.setBright(_root.helicop, 150);
                     _root.helibulletctr += 1;
                     if(_root.helibulletctr >= 6 || eval("_root." + _root.bulletArray[i]).weapontype == "rocket")
                     {
                        _root.explode_mc._x = _root.helicop._x;
                        _root.explode_mc._y = _root.helicop._y;
                        _root.explode_mc.play();
                        _root.helidestroy = true;
                        _root.dropbomb = false;
                        _root.bomb._alpha = 0;
                        _root.bomb.gotoAndStop(1);
                        _root.helibulletctr = 0;
                        _root.mscore += 50;
                        _root.txtscore.text = _root.mscore;
                        _root.score_mc.gotoAndPlay(18);
                     }
                  }
                  pi++;
               }
            }
            else
            {
               _root.bulletArray[i] = "";
            }
            if(_root.arrdeactivate == true)
            {
               break;
            }
         }
         i++;
      }
   }
}

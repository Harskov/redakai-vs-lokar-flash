// the bomb, while dropbomb is set and the helicopter is not shot down: it moves 22 a frame along degrees; on
// the bike it costs 50 points and a health frame (loose() at frame 4, else it explodes and the bike darkens);
// once delaybomb passes 10 a corner on mc_level's hit mask, or else y past 500, ends it; firebomb follows while heliactivate
onClipEvent(enterFrame){
   if(_root.dropbomb == true && _root.helidestroy != true)
   {
      this._x += 22 * Math.sin(this.degrees);
      this._y -= 22 * Math.cos(this.degrees);
      lpx = this._x - 10;
      lpy = this._y - 10;
      rpx = this._x + 10;
      rpy = this._y - 10;
      fpx = this._x + 10;
      fpy = this._y + 10;
      bpx = this._x - 10;
      bpy = this._y + 10;
      if(_root.bikeSync.mc_bike.hitTest(this))
      {
         this._x += 92 * Math.sin(this.degrees);
         this._y -= 92 * Math.cos(this.degrees);
         _root.dropbomb = false;
         _root.mscore -= 50;
         if(_root.mscore < 0)
         {
            _root.mscore = 0;
         }
         else
         {
            _root.score_mc.gotoAndPlay(34);
         }
         _root.txtscore.text = _root.mscore;
         _root.health_mc.nextFrame();
         if(_root.health_mc._currentframe >= 4)
         {
            _root.loose();
         }
         else
         {
            this.play();
            _root.bexplode = true;
            _root.setBright(_root.bikeSync.mc_bike, _root.bikedark[_root.bikedartctr]);
            _root.bikedartctr += 1;
            if(_root.heliactivate == true)
            {
               setTimeout(_root.firebomb, 2200);
            }
         }
      }
      else
      {
         _root.delaybomb += 1;
         if(_root.delaybomb > 10)
         {
            var mymov = _root.mc_level.mc.mc_hit.mask_hit_mc;
            if(mymov.hitTest(lpx, lpy, true) || mymov.hitTest(rpx, rpy, true) || mymov.hitTest(fpx, fpy, true) || mymov.hitTest(bpx, bpy, true))
            {
               this._x += 62 * Math.sin(this.degrees);
               this._y -= 62 * Math.cos(this.degrees);
               this.play();
               _root.dropbomb = false;
               if(_root.heliactivate == true)
               {
                  setTimeout(_root.firebomb, 1200);
               }
            }
         }
         else if(this._y > 500)
         {
            this.gotoAndStop(4);
            _root.dropbomb = false;
            if(_root.heliactivate == true)
            {
               setTimeout(_root.firebomb, 1200);
            }
         }
      }
   }
}

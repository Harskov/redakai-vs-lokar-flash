// the preloader bar starts empty and visible together with its background; the handler polls the load
stop();
preloader._width = 0;
preloader._visible = preloader_bg._visible = true;
// the preloader: every frame, the bar's width follows the percentage loaded, and so does txt, which
// no text field shows (a zero total is taken as 1); at 100% bar and background hide and frame 10 plays
preloader.onEnterFrame = function()
{
   filesize_total = _root.getBytesTotal();
   if(filesize_total == 0)
   {
      filesize_total = 1;
   }
   percent = Math.round(_root.getBytesLoaded() / filesize_total * 100);
   txt = percent + "%";
   preloader._width = percent * 5;
   if(percent == 100)
   {
      txt = "";
      preloader._visible = preloader_bg._visible = false;
      delete this.onEnterFrame;
      gotoAndPlay(10);
   }
};

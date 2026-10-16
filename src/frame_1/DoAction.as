// the preloader bar starts empty and visible together with its background; the handler polls the load
stop();
preloader._width = 0;
preloader._visible = preloader_bg._visible = true;
// the preloader: every frame, the bar's width and the text follow the percentage loaded
// (a zero total is taken as 1 to avoid dividing by zero); at 100% both hide and play frame 10
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

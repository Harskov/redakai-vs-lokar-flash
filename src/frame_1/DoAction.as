// the preloader bar starts empty and visible together with its background; the handler polls the load
stop();
preloader._width = 0;
preloader._visible = preloader_bg._visible = true;
preloader.onEnterFrame = function()
{ /* @reference frame_1_DoAction.onEnterFrame */ };

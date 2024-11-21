import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango, GLib

class Overlay(Gtk.Box):
    def __init__(self, show_cb, hide_cb):
        super().__init__()
        self.set_visible(True)
        self.set_opacity(1.0)

        # this is deprecated
        self.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("#ffffff"))
       
        font_desc = Pango.FontDescription("Sans Bold 48")
        self.message = Gtk.Label()
        self.message.modify_font(font_desc)
        self.pack_start(self.message, True, True, 0)

        self.show_cb = show_cb 
        self.hide_cb = hide_cb

        self.fade_interval = 20
        self.fade_step = 0.05

    def set_fade_time(self, time_ms):
        self.fade_interval = max(5, time_ms // 50)
        self.fade_step = 1.0 / (time_ms / self.fade_interval)

    def set_label(self, text):
        self.message.set_text(text)

    def start_fade_in(self, callback=None):
        self.show_cb()
        self.fade_in_opacity = 0.0 
        GLib.timeout_add(self.fade_interval, self.fade_in, callback)

    def fade_in(self, callback):
        if self.fade_in_opacity <= 1.0:
            self.set_opacity(self.fade_in_opacity)
            self.queue_draw()
            self.fade_in_opacity += self.fade_step
            return True
        else:
            if callback:
                callback()
            return False

    def start_fade_out(self, delay_ms=0):
        if delay_ms > 0:
            GLib.timeout_add(delay_ms, self._start_fade_out_animation)
        else:
            self._start_fade_out_animation()

    def _start_fade_out_animation(self):
        self.fade_out_opacity = 1.0
        GLib.timeout_add(self.fade_interval, self.fade_out)
        return False

    def fade_out(self):
        if self.fade_out_opacity >= 0.0:
            self.set_opacity(self.fade_out_opacity)
            self.queue_draw()
            self.fade_out_opacity -= self.fade_step
            return True
        else:
            self.hide_cb()
            return False


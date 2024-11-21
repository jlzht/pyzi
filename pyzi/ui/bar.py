import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

class ProgressBar(Gtk.Box):
    def __init__(self, height, width, speed=30, step_increment=0.01):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        self.set_homogeneous(True)
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_show_text(False)
        self.progress_bar.set_size_request(height, width)

        self.apply_css()

        self.pack_start(self.progress_bar, True, False, 0)

        self.current_fraction = 0.0
        self.target_fraction = 0.0
        self.step_increment = step_increment
        self.speed = speed

    def apply_css(self):
        css = """
            progressbar text {
                color: yellow;
                font-weight: bold;
            }
            progressbar trough, progress {
                border: none;
                min-height: 8px;
                border-radius: 20px;
            }
            progressbar progress {
                border: none;
                background-image: linear-gradient(90deg, #57E86B, #57E86B);
            }
        """

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css.encode())

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def reset_progress(self):
        self.progress_bar.set_fraction(0)
    
    def get_progress(self):
        return self.progress_bar.get_fraction()

    def set_progress(self, fraction, callback=None):
        self.target_fraction = fraction
        self.current_fraction = self.progress_bar.get_fraction()
        self.smooth_progress(callback)

    def smooth_progress(self, callback=None):
        if self.current_fraction < self.target_fraction:
            self.current_fraction += self.step_increment
            if self.current_fraction > self.target_fraction:
                self.current_fraction = self.target_fraction
        elif self.current_fraction > self.target_fraction:
            self.current_fraction -= self.step_increment
            if self.current_fraction < self.target_fraction:
                self.current_fraction = self.target_fraction

        self.progress_bar.set_fraction(self.current_fraction)

        if self.current_fraction != self.target_fraction:
            GLib.timeout_add(self.speed, self.smooth_progress, callback)
        else:
            if callback:
                callback()
            return False

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

class DrawingShow(Gtk.Box):
    def __init__(self, width, height, font_size, corner_radius):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        self.font_size = font_size
        self.corner_radius = corner_radius
        self.set_size_request(width, height)
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        
        self.label = Gtk.Label()
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_halign(Gtk.Align.CENTER)
        self.label.set_valign(Gtk.Align.CENTER)
        
        font_desc = Pango.FontDescription(f"Sans Bold {self.font_size}")
        self.label.modify_font(font_desc)
        
        self.pack_start(self.label, True, True, 0)
        
        self.apply_css()

    def apply_css(self):
        style_provider = Gtk.CssProvider()
        css = f"""
        .drawing-show {{
            background-color: #ffffff;
            border-radius: {self.corner_radius}px;
            padding: 10px;
        }}
        """
        style_provider.load_from_data(css.encode())
        
        style_context = self.get_style_context()
        style_context.add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        style_context.add_class("drawing-show")

class CharacterShow(DrawingShow):
    def __init__(self):
        super().__init__(width=300, height=300, font_size=100, corner_radius=15)

    def set_label(self, label):
        self.label.set_text(label)
        self.queue_draw()

class PinyinShow(DrawingShow):
    def __init__(self):
        super().__init__(width=300, height=36, font_size=12, corner_radius=10)

    def set_label(self, label):
        text = label if label else "---"
        self.label.set_text(text)
        self.queue_draw()

class CompoundShow(DrawingShow):
    def __init__(self):
        super().__init__(width=300, height=36, font_size=12, corner_radius=10)

    def set_label(self, label):
        text = " + ".join(label) if label else "---"
        self.label.set_text(text)
        self.queue_draw()


import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango

from .button import ResetButton
from .bar import ProgressBar
from pyzi.tape import Tape

class Level(Gtk.Box):
    DESCRIPTION = Pango.FontDescription("Sans Bold 64")

    def __init__(self, level, initial, session, cursor, load_callback):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
       
        self.initial = initial
        self.session = session
        self.cursor = cursor

        button = Gtk.Button()
        
        label = Gtk.Label(label=level)
        label.modify_font(Level.DESCRIPTION)

        button.get_style_context().add_class("level")
        button.add(label)
        button.set_size_request(150, 150)

        button.connect("clicked", lambda btn: load_callback(self.session, cursor))

        self.apply_css()

        deck = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        reset = ResetButton("object-rotate-right-symbolic")
        reset.set_callback(self.reset)

        self.progress = ProgressBar(100, 12, 20)
        
        deck.add(self.progress)
        deck.add(reset)

        self.pack_start(button, False, False, 0)
        self.pack_start(deck, False, False, 0)

    def reset(self, widget: Gtk.Button):
        self.session.clear()
        self.session.update(self.initial) 
        self.cursor = 0
        self.update()

    def update(self):
        value = sum(self.session.values()) / (len(self.session) * Tape.THRESHOLD)
        self.progress.set_progress(value, None)

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        css = """

        .level-box {
            background-color: #f2f2f2;
            padding: 20px;
            border-radius: 10px;
        }

        .level {
            background: #ffffff;
            border: none;
            box-shadow: none;
            border-radius: 12px;
        }

        .level:focus {
            outline: none;
        }

        .level:active {
            background-color: #1abc9c;
        }
        """
        css_provider.load_from_data(css.encode("utf-8"))

        screen = Gdk.Screen.get_default()
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


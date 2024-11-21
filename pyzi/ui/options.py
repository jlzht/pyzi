import random

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Options(Gtk.Grid):
    def __init__(self, callback):
        super().__init__()
        self.set_row_spacing(12)
        self.set_column_spacing(12)

        self.options = [OptionButton(callback) for _ in range(4)]

        for i, option in enumerate(self.options):
            self.attach(option, i % 2, i // 2, 1, 1)

        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)

    def clear(self):
        for option in self.options:
            option.set_label("")
            option.selected = False

    def disable(self):
        for option in self.options:
            option.disable()

    def update(self, options):
        self.clear()
        randomized = options[:]
        random.shuffle(randomized)

        for i, option in enumerate(self.options):
            option.set_label(randomized[i])
            if option.get_label() == options[0]:
                option.selected = True

class OptionButton(Gtk.Button):
    def __init__(self, callback):
        super().__init__()
        self.set_size_request(144, 50)
        self.connect("clicked", self.select)
        self.callback = callback
        self.selected = False
        self.apply_css()
    
    def select(self, widget):
        self.callback(self.selected)

    def disable(self):
        self.set_sensitive(False)

    def enable(self):
        self.set_sensitive(True)

    def apply_css(self):
        css_provider = Gtk.CssProvider()

        css = """
        button {
            background: white;
            background-color: white;
            color: black;
            border: none;
            box-shadow: none;
            border-radius: 15px;
            font-size: 16px;
            padding: 0px;
        }

        button:active {
            background-color: #1abc9c;
        }

        """

        css_provider.load_from_data(css.encode())

        style_context = self.get_style_context()
        style_context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

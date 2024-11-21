import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .button import CyclerButton

class Cycler(Gtk.Box):
    ICON_SIZE = 16
    CLASSES = [
        "Animal",
        "Food",
        "Body",
        "Weather",
        "Time",
        "Emotion",
        "Color",
        "Nature",
        "Space",
        "Clothing",
        "Building",
        "Tool",
        "Skill",
        "Action",
        "Quantity",
        "Person",
        "Connector",
        "Location"
    ]

    def __init__(self):
        super().__init__(spacing=8, orientation=Gtk.Orientation.HORIZONTAL)
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        
        self.cursor = 0

        self.prev_button = CyclerButton("go-previous-symbolic") 
        self.prev_button.set_callback(self.on_prev_clicked)
        self.pack_start(self.prev_button, False, False, 0)
        
        self.label = Gtk.Label(label=self.CLASSES[self.cursor])
        self.label.set_size_request(80, -1)
        self.pack_start(self.label, True, True, 0)

        self.next_button = CyclerButton("go-next-symbolic") 
        self.next_button.set_callback(self.on_next_clicked)
        self.pack_start(self.next_button, False, False, 0)
        
    def get_label(self):
        return self.CLASSES[self.cursor]

    def on_prev_clicked(self, widget: Gtk.Button):
        self.cursor = (self.cursor - 1) % len(self.CLASSES)
        self.label.set_text(self.CLASSES[self.cursor])

    def on_next_clicked(self, widget: Gtk.Button):
        self.cursor = (self.cursor + 1) % len(self.CLASSES)
        self.label.set_text(self.CLASSES[self.cursor])

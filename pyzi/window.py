import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .ui.screen import GameScreen, MenuScreen, InfoScreen
from .ui.overlay import Overlay

class Window(Gtk.Window):
    def __init__(self, levels):
        super().__init__(title="Pyzi")
        self.set_default_size(800, 600)

        self.game = GameScreen()
        self.menu = MenuScreen(levels, self.game.load_session)
        self.info = InfoScreen()

        self.main = Gtk.Overlay()
        self.add(self.main)
        
        self.screens = {"menu": self.menu, "game": self.game, "info": self.info}
        self.overlay = Overlay(self.show_overlay, self.hide_overlay)

        self.show_overlay()
        self.overlay.start_fade_out()

        for screen in self.screens.values():
            screen.set_transition(self.set_screen)

        self.main.add(self.screens["menu"])
        self.prev = None
        self.curr = "menu"
        
        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def clear(self):
        for child in list(self.main.get_children()):
            if child.get_name() in self.screens:
                self.main.remove(child)
    
    # revisit this
    def set_screen(self, name, speed, delay=0, message=None):
        val = name if name != "back" else self.prev

        def callback():
            self.clear()
            if val in self.screens:
                if not (name == "back" and self.prev == "game" and self.curr == "info"):
                    self.screens[val].update()
                self.main.add(self.screens[val])
            
            # Special case
            if name == "back" and self.prev == "game" and self.curr == "info":
                self.prev = "menu"
                self.curr = "game" 
            else:
                self.prev = self.curr
                self.curr = val
            self.show_all()
            self.overlay.start_fade_out(delay)

        self.overlay.set_fade_time(speed)
        self.overlay.set_label(message or "")
        self.overlay.start_fade_in(callback)

    def show_overlay(self):
        self.main.add_overlay(self.overlay)

    def hide_overlay(self):
        self.main.remove(self.overlay)

from pyzi.parser import Parser
from pyzi.window import Window

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def main():
    levels = Parser.load_levels()
    Window(levels)
    Gtk.main()
    print(levels)
    Parser.save_levels(levels)

if __name__ == "__main__":
    main()

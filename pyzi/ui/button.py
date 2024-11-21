import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class CustomButton(Gtk.Button):
    def __init__(self, symbol: str, icon_size: int = 16):
        super().__init__()
        self.icon_size = icon_size

        self.apply_css()

        button_image = self.create_button(symbol)
        self.add(button_image)
        self.set_size_request(-1, -1)

    def set_callback(self, callback):
        self.connect("clicked", callback)

    def create_button(self, icon_name: str) -> Gtk.Image:
        icon_theme = Gtk.IconTheme.get_default()
        icon_pixbuf = icon_theme.load_icon(icon_name, self.icon_size, 0)

        if icon_pixbuf:
            return Gtk.Image.new_from_pixbuf(icon_pixbuf)

        return Gtk.Image.new_from_icon_name("view-refresh-symbolic", Gtk.IconSize.BUTTON)

    def apply_css(self):
        pass

    def add_custom_css_class(self):
        pass

class CyclerButton(CustomButton):
    def __init__(self, symbol: str):
        super().__init__(symbol, icon_size=16)
        self.apply_css()

    def apply_css(self):
        css_provider = Gtk.CssProvider()

        css = """
        .cycler {
            background: #ffffff;
            color: black;
            border: none;
            box-shadow: none;
            border-radius: 32px;
        }
    
        .cycler:focus {
            outline: none;
        }
        """
        css_provider.load_from_data(css.encode())

        screen = Gdk.Screen.get_default()
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        self.get_style_context().add_class("cycler")

class ResetButton(CustomButton):
    def __init__(self, symbol: str):
        super().__init__(symbol, icon_size=12)
        self.apply_css()

    def apply_css(self):
        css_provider = Gtk.CssProvider()

        css = """
        .reset {
            background-color: transparent;
            background-image: none;
            border: none;
            box-shadow: none;
        }

        .reset:active {
            color: red;
        }
    
        .reset:focus {
            outline: none;
        }
        """
        css_provider.load_from_data(css.encode())

        screen = Gdk.Screen.get_default()
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        self.get_style_context().add_class("reset")

class ActionButton(CustomButton):
    def __init__(self, symbol: str):
        super().__init__(symbol, icon_size=16)
        self.apply_css()

    def apply_css(self):
        css_provider = Gtk.CssProvider()

        css = """
        .action {
            background: #ffffff;
            color: black;
            border: none;
            box-shadow: none;
            border-radius: 32px;
        }

        .action:focus {
            outline: none;
        }
        """
        css_provider.load_from_data(css.encode())

        screen = Gdk.Screen.get_default()
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        self.get_style_context().add_class("action")

#import gi
#gi.require_version("Gtk", "3.0")
#from gi.repository import Gtk, Gdk

#class CustomButton(Gtk.Button):
#    def __init__(self, symbol: str, icon_size: int = 16):
#        super().__init__()
#        self.icon_size = icon_size
#
#        self.apply_css()
#
#        button_image = self.create_button(symbol)
#        self.add(button_image)
#        self.set_size_request(-1, -1)
#
#    def set_callback(self, callback):
#        self.connect("clicked", callback)
#
#    def create_button(self, icon_name: str) -> Gtk.Image:
#        icon_theme = Gtk.IconTheme.get_default()
#        icon_pixbuf = icon_theme.load_icon(icon_name, self.icon_size, 0)
#
#        if icon_pixbuf:
#            return Gtk.Image.new_from_pixbuf(icon_pixbuf)
#
#        return Gtk.Image.new_from_icon_name("view-refresh-symbolic", Gtk.IconSize.BUTTON)
#
#    def apply_css(self):
#        pass

#class CyclerButton(CustomButton):
#    def __init__(self, symbol: str):
#        super().__init__(symbol, icon_size=16)
#        self.apply_css()
#
#    def apply_css(self):
#        self.get_style_context().add_class("cycler")
#
#class ResetButton(CustomButton):
#    def __init__(self, symbol: str):
#        super().__init__(symbol, icon_size=12)
#        self.apply_css()
#
#    def apply_css(self):
#        self.get_style_context().add_class("reset")
#
#class ActionButton(CustomButton):
#    def __init__(self, symbol: str):
#        super().__init__(symbol, icon_size=16)
#        self.apply_css()
#
#    def apply_css(self):
#        self.get_style_context().add_class("action")

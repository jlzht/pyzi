from .cycler import Cycler
from .overlay import Overlay
from .bar import ProgressBar
from .panel import CharacterShow, PinyinShow, CompoundShow
from .level import Level
from .button import ActionButton
from .options import Options

from pyzi.parser import Parser
from pyzi.tape import Tape 

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango

class AbstractScreen(Gtk.Box):
    def __init__(self, orientation, spacing, css_class=None):
        super().__init__(orientation=orientation, spacing=spacing)
        self.callback = None
        if css_class:
            self.apply_css(css_class)

    def set_transition(self, callback):
        self.callback = callback

    def add_back_button(self):
        undo = ActionButton("edit-undo-symbolic")
        undo.set_valign(Gtk.Align.START)
        undo.set_halign(Gtk.Align.START)
        undo.set_margin_top(9)
        undo.set_margin_left(9)
        undo.set_callback(lambda btn: self.callback("back", 600))
        self.pack_start(undo, False, False, 0)

    def add_info_button(self):
        info = ActionButton("help-about-symbolic")
        info.set_valign(Gtk.Align.END)
        info.set_halign(Gtk.Align.END)
        info.set_margin_bottom(9)
        info.set_margin_right(9)
        info.set_callback(lambda btn: self.callback("info", 1200))
        self.pack_start(info, False, False, 0)

    def apply_css(self, css_class):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(f"""
            .{css_class} {{
                background-color: #c2c2c2;
                padding: 20px;
                border-radius: 10px;
            }}
            .rounded {{
                background-color: #eeeeee;
                border-radius: 15px;
                font-size: 14px;
                padding: 10px;
            }}
        """.encode("utf-8"))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

class GameScreen(AbstractScreen):
    def __init__(self):
        super().__init__(Gtk.Orientation.HORIZONTAL, 0, "game")
        self.set_name("game")

        self.graph = Parser.load_graph()
        self.tape = Tape()
        self.target = None
        self.progress = ProgressBar(280, 20, 30)
        self.character = CharacterShow()
        self.compound = CompoundShow()
        self.pinyin = PinyinShow()
        self.options = Options(self.verify)
        self.cycler = Cycler()

        self.winned = False

        self.add_back_button()
        self.add_vbox_widget()
        self.add_info_button()

    def add_vbox_widget(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_halign(Gtk.Align.CENTER)
        vbox.set_valign(Gtk.Align.CENTER)

        for widget in [self.progress, self.character, self.compound, self.pinyin, self.options, self.cycler]:
            vbox.pack_start(widget, False, False, 0)
        
        self.pack_start(vbox, True, True, 0)

    def load_session(self, session, cursor):

        self.target = None
        self.tape.load(session, cursor)

        value = self.tape.get_progress()
        if not value == 1.0:
            self.callback("game", 600)
            self.clear()
            self.progress.set_progress(value, None)

    def clear(self):
        self.progress.reset_progress()
        self.character.set_label("")
        self.compound.set_label("")
        self.pinyin.set_label("")
        self.options.clear()

    def update(self):
        value = None
        
        if not self.winned:
            if self.target == None:
                value, data = self.tape.current()
                if data >= 2:
                    value, _ = self.tape.next()
            else:
                value, _ = self.tape.next()
        else:
            self.callback("menu", 1200, 1000, "Level Completed")
            self.winned = False

        self.target = self.graph.get_node(value)

        self.character.set_label(self.target['character'])
        self.compound.set_label(self.target['compound'])
        self.pinyin.set_label(self.target['pinyin'])

        meanings = self.graph.get_options(self.target)
        self.options.update(meanings)

    def verify(self, correct):
        target = self.target['class'].strip()
        option = self.cycler.get_label().strip()
        self.tape.verify(target == option and correct)
        value = self.tape.get_progress()
        # lame fix
        if value == 1.0:
            self.winned = True
        self.progress.set_progress(value, self.update)

class MenuScreen(AbstractScreen):
    def __init__(self, levels, load_callback):
        super().__init__(Gtk.Orientation.VERTICAL, 0, "menu")
        self.set_name("menu")

        self.levels = [Level(level[0], level[1], level[2], level[3], load_callback) for level in levels]
       
        font_desc = Pango.FontDescription("Sans Bold 52")
        message = Gtk.Label("P学zi")
        message.modify_font(font_desc)
        message.set_valign(Gtk.Align.START)
        self.pack_start(message, True, True, 0)
        self.add_main_widget()
        self.add_info_button()

    def add_main_widget(self):

        box = Gtk.Box(spacing=12, orientation=Gtk.Orientation.VERTICAL)
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.START)
        box.get_style_context().add_class("rounded")

        main = Gtk.Box(spacing=10, orientation=Gtk.Orientation.HORIZONTAL)
        main.set_size_request(640, -1)
        main.get_style_context().add_class("back-box")
        
        box.add(main)
        
        for level in self.levels:
            level.update()
            main.pack_start(level, True, False, 0)

        self.pack_start(box, True, True, 0)

    # TODO: lock completed levels
    def update(self):
        for level in self.levels:
            level.update()

class InfoScreen(AbstractScreen):
    TUTORIAL = """
    <b>Objective:</b>
    Your goal is to correctly identify the category of the displayed Chinese character.
    
    <b>What You’ll See:</b>
    <b>Character:</b> A Chinese character will be shown at the center of the screen.
    <b>Romanization:</b> The pinyin (romanized pronunciation) of the character is provided.
    <b>Kangxi Radicals:</b> The traditional building blocks of the character are displayed to help you
    analyze its structure and meaning.
    
    <b>Your Task:</b>
    - Use the slider to select the category that best matches the character. Categories might include its
        meaning, usage, or grammatical role.
    - You will have four options to choose from—pick the one that fits best!
    """

    def __init__(self):
        super().__init__(Gtk.Orientation.VERTICAL, 20, "info")
        self.set_name("info")

        self.add_back_button()
        self.add_main_widget()

    def add_main_widget(self):

        label = Gtk.Label()
        label.set_markup(InfoScreen.TUTORIAL)
        label.set_line_wrap(True)
        label.set_line_wrap_mode(Pango.WrapMode.WORD)
        label.set_justify(Gtk.Justification.LEFT)
        label.set_halign(Gtk.Align.FILL)
        label.set_valign(Gtk.Align.FILL)

        main = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        main.set_size_request(640, 220)
        main.set_halign(Gtk.Align.CENTER)
        main.set_valign(Gtk.Align.CENTER)
        main.get_style_context().add_class("rounded")

        main.pack_start(label, True, True, 0)

        self.pack_start(main, True, True, 0)

    def update(self):
        pass

from ..Env import FILE_CACHE_CSS
from ..Imports import *


class Style:
    def __init__(self, css_path):
        self.css_provider = Gtk.CssProvider()
        self.__transpile_scss(css_path)
        self.__load_css(self.css_provider, self.css_path)
        self.__apply_style(self.css_provider)

    def __transpile_scss(self, css_path):
        if css_path.endswith(".scss"):
            if GLib.file_test(self.css_path, GLib.FileTest.EXISTS):
                GLib.spawn_command_line_sync(f"rm {self.css_path}")

            try:
                if css_path.startswith("./"):
                    _, out, _, _ = GLib.spawn_command_line_sync("pwd")
                    current_dir = out.decode("utf-8").replace("\n", "")
                    css_path = GLib.build_filenamev([current_dir, css_path[2:]])

                GLib.spawn_command_line_sync(f"sassc {css_path} {self.css_path} ")
            except Exception as e:
                print(f"Error transpiling SCSS:")
                print(e)

    def __load_css(self, css_provider, css_path):
        try:
            css_provider.load_from_path(css_path)
        except Exception as e:
            print(f"Error loading CSS file:")
            print(e)

    def __apply_style(self, css_provider):
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

from ..Env import FILE_CACHE_CSS
from ..Imports import *
from ..Methods import lookup_icon, parse_interval, wait
from .Service import *


class Style(Service):
    @staticmethod
    def load_css(css_path) -> None:

        if css_path.endswith(".scss"):
            try:
                if GLib.file_test(FILE_CACHE_CSS, GLib.FileTest.EXISTS):
                    GLib.spawn_command_line_sync(f"rm {FILE_CACHE_CSS}")

                GLib.spawn_command_line_sync(f"sassc {css_path} {FILE_CACHE_CSS} ")

            except Exception as e:
                print(f"Error transpiling SCSS:")
                print(e)
        try:
            css_provider = Gtk.CssProvider()
            css_provider.load_from_path(css_path)

            screen: Gdk.Screen = Gdk.Screen.get_default()
            style_context: Gtk.StyleContext = Gtk.StyleContext()
            style_context.add_provider_for_screen(screen, css_provider, 600)
        except Exception as e:
            print(f"Error loading CSS file:")
            print(e)

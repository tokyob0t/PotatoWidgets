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
        else:
            pass

        try:
            # Load Provider
            css_provider = Gtk.CssProvider()
            # Load File
            css_provider.load_from_path(FILE_CACHE_CSS)

            # Get Default Screen
            screen: Gdk.Screen = Gdk.Screen.get_default()
            # Get StyleConext
            style_context: Gtk.StyleContext = Gtk.StyleContext()
            # Load Provider
            style_context.add_provider_for_screen(
                screen=screen, provider=css_provider, priority=600
            )
        except Exception as e:
            print(f"Error loading CSS file:")
            print(e)

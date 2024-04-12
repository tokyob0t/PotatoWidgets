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

    @staticmethod
    def rgb(red, green, blue):
        return "#{:02x}{:02x}{:02x}".format(red, green, blue)

    @staticmethod
    def rgba(red, green, blue, alpha):
        alpha = round(alpha * 255)
        return "#{:02x}{:02x}{:02x}{:02x}".format(red, green, blue, alpha)

    @staticmethod
    def mix(color_1, color_2, percentage):
        if percentage < 0 or percentage > 1:
            raise ValueError("El porcentaje debe estar entre 0 y 1")

        r1, g1, b1 = int(color_1[1:3], 16), int(color_1[3:5], 16), int(color_1[5:7], 16)
        r2, g2, b2 = int(color_2[1:3], 16), int(color_2[3:5], 16), int(color_2[5:7], 16)

        r = round(r1 * (1 - percentage) + r2 * percentage)
        g = round(g1 * (1 - percentage) + g2 * percentage)
        b = round(b1 * (1 - percentage) + b2 * percentage)

        return Style.rgb(r, g, b)

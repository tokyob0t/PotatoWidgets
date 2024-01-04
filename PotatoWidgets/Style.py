from .__Import import *


class Style:
    def __init__(self, css_path):
        self.cache_dir = GLib.get_user_cache_dir() + "/potatowidgets"
        GLib.mkdir_with_parents(self.cache_dir, 0o755)

        self.css_path = self.__transpile_scss(css_path)
        self.css_provider = Gtk.CssProvider()
        self.__load_css(self.css_provider, self.css_path)
        self.__apply_style(self.css_provider)

    def __transpile_scss(self, css_path):
        if css_path.endswith(".scss"):
            css_filename = css_path.split("/")[-1].replace(".scss", ".css")
            css_path = f"{self.cache_dir}/{css_filename}"

            if GLib.file_test(css_path, GLib.FileTest.EXISTS):
                GLib.file_delete(css_path)

            try:
                GLib.spawn_command_line_sync(
                    f"sassc {css_path.replace('.css', '.scss')} {css_path}"
                )
            except Exception as e:
                print(f"Error transpiling SCSS: {e}")

        return css_path

    def __load_css(self, css_provider, css_path):
        try:
            css_provider.load_from_path(css_path)
        except Exception as e:
            print(f"Error loading CSS file: {e}")

    def __apply_style(self, css_provider):
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

from .__Import import *


class Style:
    def __init__(self, scss_path):
        self.cache_dir = os.path.expanduser("~/.cache/potatowidgets")
        os.makedirs(self.cache_dir, exist_ok=True)

        self.css_path = self.transpile_scss(scss_path)
        self.css_provider = Gtk.CssProvider()
        self.load_css(self.css_provider, self.css_path)
        self.apply_style(self.css_provider)

    def transpile_scss(self, scss_path):
        css_filename = os.path.basename(scss_path).replace(".scss", ".css")
        css_path = os.path.join(self.cache_dir, css_filename)

        if os.path.exists(css_path):
            os.remove(css_path)

        try:
            run(["sassc", scss_path, css_path], check=True, stdout=PIPE, stderr=PIPE)
        except Exception as e:
            print(f"Error transpiling SCSS: {e}")

        return css_path

    def load_css(self, css_provider, css_path):
        try:
            css_provider.load_from_path(css_path)
        except Exception as e:
            print(f"Error loading CSS file: {e}")

    def apply_style(self, css_provider):
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def add_class(self, widget, class_name):
        widget.get_style_context().add_class(class_name)

    def remove_class(self, widget, class_name):
        widget.get_style_context().remove_class(class_name)

    def set_property(self, widget, property_name, value):
        widget.get_style_context().set_property(property_name, value)

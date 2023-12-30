from ...__Import import *


class BasicProps(Gtk.Widget, Gtk.CssProvider):
    def __init__(
        self,
        halign,
        valign,
        hexpand,
        vexpand,
        active,
        visible,
        classname,
        size=[10, 10],
    ):
        self.set_hexpand(True if hexpand else False)
        self.set_vexpand(True if vexpand else False)
        self.set_halign(self.__clasif_align(halign))
        self.set_valign(self.__clasif_align(valign))
        self.set_visible(visible)
        self.set_sensitive(active) if active != None else None

        [self.set_css_name(i) for i in classname.split(" ") if i != " "]

        if isinstance(size, int):
            self.set_size_request(size, size)
        elif isinstance(size, list):
            if len(size) == 2:
                self.set_size_request(size[0], size[1])
            elif len(size) == 1:
                self.set_size_request(size[0], size[0])

    def __clasif_align(self, param):
        dict = {
            "fill": Gtk.Align.FILL,
            "start": Gtk.Align.START,
            "end": Gtk.Align.END,
            "center": Gtk.Align.CENTER,
            "baseline": Gtk.Align.BASELINE,
        }
        return dict.get(param.lower(), Gtk.Align.FILL)

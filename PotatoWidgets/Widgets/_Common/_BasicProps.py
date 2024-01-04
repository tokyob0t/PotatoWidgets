from ...__Import import *
from ...Variable import Listener, Poll, Variable


class BasicProps(Gtk.Widget):
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
        Gtk.Widget.__init__(self)
        self.set_hexpand(True if hexpand else False)
        self.set_vexpand(True if vexpand else False)
        self.set_halign(self.__clasif_align(halign))
        self.set_valign(self.__clasif_align(valign))
        self.set_visible(visible)
        self.set_sensitive(active) if active is not None else None
        self.__clasif_size(size)

        # [self.set_css_name(i) for i in classname.split(" ") if i != " "]

        for key, value in locals().items():
            if isinstance(value, (Listener, Poll, Variable)):
                if key == "halign":
                    value.connect(
                        "valuechanged",
                        lambda x: GLib.idle_add(
                            lambda: self.set_halign(self.__clasif_align(str(x)))
                        ),
                    )
                elif key == "valign":
                    value.connect(
                        "valuechanged",
                        lambda x: GLib.idle_add(
                            lambda: self.set_valign(self.__clasif_align(str(x)))
                        ),
                    )
                elif key == "hexpand":
                    value.connect(
                        "valuechanged",
                        lambda x: GLib.idle_add(
                            lambda: self.set_hexpand(True if x else False)
                        ),
                    )
                elif key == "vexpand":
                    value.connect(
                        "valuechanged",
                        lambda x: GLib.idle_add(
                            lambda: self.set_vexpand(True if x else False)
                        ),
                    )
                elif key == "active":
                    value.connect(
                        "valuechanged",
                        lambda x: GLib.idle_add(lambda: self.set_sensitive(x)),
                    )
                elif key == "visible":
                    value.connect(
                        "valuechanged",
                        lambda x: GLib.idle_add(lambda: self.set_visible(x)),
                    )
                elif key == "classname":
                    value.connect(
                        "valuechanged",
                        lambda x: GLib.idle_add(
                            lambda: [
                                self.set_css_name(i) for i in x.split(" ") if i != " "
                            ]
                        ),
                    )
                elif key == "size":
                    value.connect(
                        "valuechanged", lambda x: GLib.idle_add(self.__clasif_size(x))
                    )

    def __clasif_size(self, size):
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

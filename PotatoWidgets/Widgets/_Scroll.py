from ..__Import import *
from ..Variable import Listener, Poll, Variable
from ._Common._BasicProps import BasicProps


class Scroll(Gtk.ScrolledWindow, BasicProps):
    def __init__(
        self,
        orientation="h",
        children=None,
        attributes=None,
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        visible=True,
        classname="",
    ):
        Gtk.ScrolledWindow.__init__(self)
        BasicProps.__init__(
            self,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=None,
            visible=visible,
            classname=classname,
        )

        self.__clasif_orientation(orientation)
        self.set_visible(visible)
        self.add_with_viewport(children) if children else None

        attributes(self) if attributes else None
        for key, value in locals().items():
            if key not in [
                "self",
                "halign",
                "valign",
                "hexpand",
                "vexpand",
                "visible",
                "active",
                "visible",
                "classname",
            ] and isinstance(value, (Listener, Poll, Variable)):
                if key == "orientation":
                    value.connect(
                        "valuechanged",
                        lambda x: GLib.idle_add(lambda: self.set_orientation(x)),
                    )
                elif key == "visible":
                    value.connect(
                        "valuechanged",
                        lambda x: GLib.idle_add(lambda: self.set_visible(x)),
                    )
                elif key == "children":
                    value.connect(
                        "children",
                        lambda x: GLib.idle_add(lambda: self.add_with_viewport(x)),
                    )

    def set_orientation(self, param):
        super().set_orientation(self.__clasif_orientation(param))

    def __clasif_orientation(self, orientation):
        if orientation.lower() in ["vertical", "v", 0, False]:
            return Gtk.Orientation.VERTICAL
        elif orientation.lower() in ["horizontal", "h", 1, True]:
            return Gtk.Orientation.HORIZONTAL

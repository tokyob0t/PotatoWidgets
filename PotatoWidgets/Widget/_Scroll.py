from ..__Import import *
from ..Variable import Listener, Poll, Variable
from ._Common._BasicProps import BasicProps


class Scroll(Gtk.ScrolledWindow, BasicProps):
    def __init__(
        self,
        children=Gtk.Box(),
        attributes=lambda self: self,
        orientation="h",
        css="",
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
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=None,
            visible=visible,
            classname=classname,
        )

        self.set_children(children)
        self.set_orientation(orientation)
        self.set_visible(visible)

        attributes(self)
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
                callback = {
                    "orientation": self.set_orientation,
                    "visible": self.set_visible,
                    "children": self.add_with_viewport,
                }.get(key)

                self.bind(value, callback) if callback else None

    def set_orientation(self, orientation):
        super().set_orientation(self.__clasif_orientation(orientation))

    def __clasif_orientation(self, orientation):
        if orientation.lower() in ["vertical", "v", 0, False]:
            return Gtk.Orientation.VERTICAL
        elif orientation.lower() in ["horizontal", "h", 1, True]:
            return Gtk.Orientation.HORIZONTAL

    def set_children(self, children):
        if children:
            super().add_with_viewport(children)

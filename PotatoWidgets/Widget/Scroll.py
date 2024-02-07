from ..Imports import *
from .Common import BasicProps
from ..Variable import Listener, Poll, Variable


class Scroll(Gtk.ScrolledWindow, BasicProps):
    def __init__(
        self,
        children=None,
        attributes=None,
        orientation="h",
        size=[0],
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
            size=size,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=True,
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
                callback = {
                    "orientation": self.set_orientation,
                    "visible": self.set_visible,
                    "children": self.add_with_viewport,
                }.get(key)

                self.bind(value, callback) if callback else None

    def set_orientation(self, param):
        super().set_orientation(self.__clasif_orientation(param))

    def __clasif_orientation(self, orientation):
        if orientation.lower() in ["vertical", "v", 0, False]:
            return Gtk.Orientation.VERTICAL
        elif orientation.lower() in ["horizontal", "h", 1, True]:
            return Gtk.Orientation.HORIZONTAL

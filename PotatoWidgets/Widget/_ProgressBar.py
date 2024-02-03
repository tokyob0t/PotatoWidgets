from ..__Import import *
from ._Common._BasicProps import BasicProps


class ProgressBar(Gtk.ProgressBar, BasicProps):
    def __init__(
        self,
        value=50,
        inverted=False,
        orientation="h",
        attributes=lambda self: self,
        css="",
        classname="",
        halign="fill",
        valign="fill",
        size=10,
        hexpand=False,
        vexpand=False,
        visible=True,
    ):
        Gtk.Scale.__init__(self)
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
            size=size,
        )

        self.set_value(value)
        self.set_inverted(inverted)
        self.set_orientation(orientation)

        attributes(self)

    def set_value(self, value):
        self.set_fraction(value / 100)

    def set_orientation(self, param):
        return super().set_orientation(self.__clasif_orientation(param))

    def __clasif_orientation(self, orientation):
        if orientation.lower() in ["vertical", "v", 0, False]:
            return Gtk.Orientation.VERTICAL
        elif orientation.lower() in ["horizontal", "h", 1, True]:
            return Gtk.Orientation.HORIZONTAL

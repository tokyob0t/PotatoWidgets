from ..__Import import *
from ._Common._BasicProps import BasicProps


class Scroll(Gtk.ScrolledWindow, BasicProps):
    def __init__(
        self,
        orientation="h",
        children=[],
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

    def __clasif_orientation(self, orientation):
        if orientation.lower() in ["vertical", "v", 0, False]:
            return Gtk.Orientation.VERTICAL
        elif orientation.lower() in ["horizontal", "h", 1, True]:
            return Gtk.Orientation.HORIZONTAL

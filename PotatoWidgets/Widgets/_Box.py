from ..__Import import *
from ._Common._BasicProps import BasicProps


class Box(Gtk.Box, BasicProps):
    def __init__(
        self,
        orientation="h",
        spacing=0,
        homogeneous=False,
        children=[],
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        visible=True,
        classname="",
    ):
        Gtk.Box.__init__(self)
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

        self.set_orientation(self.__clasif_orientation(orientation))
        self.set_visible(visible)
        self.set_spacing(spacing)
        self.set_homogeneous(homogeneous) if homogeneous in [True, False] else None

        [self.add(i) for i in children]

    def __clasif_orientation(self, orientation):
        if orientation.lower() in ["vertical", "v", 0, False]:
            return Gtk.Orientation.VERTICAL
        elif orientation.lower() in ["horizontal", "h", 1, True]:
            return Gtk.Orientation.HORIZONTAL

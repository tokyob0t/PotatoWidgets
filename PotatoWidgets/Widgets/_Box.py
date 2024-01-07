from ..__Import import *
from ..Variable import Listener, Poll, Variable
from ._Common._BasicProps import BasicProps


class Box(Gtk.Box, BasicProps):
    def __init__(
        self,
        children=[],
        orientation="h",
        spacing=0,
        homogeneous=False,
        attributes=None,
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

        self.set_orientation(orientation)
        self.set_visible(visible)
        self.set_spacing(spacing)
        self.set_homogeneous(homogeneous) if homogeneous else None
        # self.set_halign(halign)
        # self.set_valign(valign)
        [self.add(i) for i in children] if children else None

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
                    "spacing": self.set_spacing,
                    "homogeneous": self.set_homogeneous,
                    "children": self.set_children,
                }.get(key)

                self.bind(value, callback) if callback else None

    def set_orientation(self, param):
        return super().set_orientation(self.__clasif_orientation(param))

    def set_children(self, newChildrenList=[]):
        if not newChildrenList:
            return

        for i in self.get_children():
            if i not in newChildrenList:
                i.destroy()
            self.remove(i)

        [self.add(i) for i in newChildrenList]
        self.show_all()

    def __clasif_orientation(self, orientation):
        if orientation.lower() in ["vertical", "v", 0, False]:
            return Gtk.Orientation.VERTICAL
        elif orientation.lower() in ["horizontal", "h", 1, True]:
            return Gtk.Orientation.HORIZONTAL

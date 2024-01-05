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
                if key == "orientation":
                    value.connect(
                        "valuenchanged",
                        lambda x: GLib.idle_add(lambda: self.set_orientation(x)),
                    )
                elif key == "visible":
                    value.connect(
                        "valuenchanged",
                        lambda x: GLib.idle_add(lambda: self.set_visible(x)),
                    )
                elif key == "spacing":
                    value.connect(
                        "valuenchanged",
                        lambda x: GLib.idle_add(lambda: self.set_spacing(x)),
                    )
                elif key == "homogeneous":
                    value.connect(
                        "valuenchanged",
                        lambda x: GLib.idle_add(lambda: self.set_homogeneous(x)),
                    )

    def set_orientation(self, param):
        return super().set_orientation(self.__clasif_orientation(param))

    def __clasif_orientation(self, orientation):
        if orientation.lower() in ["vertical", "v", 0, False]:
            return Gtk.Orientation.VERTICAL
        elif orientation.lower() in ["horizontal", "h", 1, True]:
            return Gtk.Orientation.HORIZONTAL

    @property
    def children(self):
        return self.get_children()

    @children.setter
    def children(self, newChildrenList=[]):
        if not newChildrenList:
            return

        for i in self.get_children():
            if i not in newChildrenList:
                i.destroy()
            else:
                self.remove(i)

        [self.add(i) for i in newChildrenList]

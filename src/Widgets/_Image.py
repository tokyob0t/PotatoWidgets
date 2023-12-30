from ..__Import import *
from ._Common._BasicProps import BasicProps


class Image(Gtk.Image, BasicProps):
    def __init__(
        self,
        path="",
        size=[20],
        halign="fill",
        valign="fill",
        visible=True,
        classname="",
    ):
        Gtk.Image.__init__(self)
        BasicProps.__init__(
            self,
            halign=halign,
            valign=valign,
            hexpand=False,
            vexpand=False,
            active=True,
            visible=visible,
            classname=classname,
            size=size,
        )
        self.set_from_file(path)

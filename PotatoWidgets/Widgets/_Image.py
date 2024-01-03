from ..__Import import *
from ..Variable import Listener, Poll, Variable
from ._Common._BasicProps import BasicProps


class Image(Gtk.Image, BasicProps):
    def __init__(
        self,
        path="",
        size=20,
        halign="fill",
        valign="fill",
        visible=True,
        classname="",
        attributes=None,
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
        self.size = size
        self.path = path
        self.__reload_image()
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
                if key == "path":
                    value.connect(
                        "valuechanged",
                        lambda x: GLib.idle_add(lambda: self.set_path(x)),
                    )
                    self.__reload_image()
                elif key == "size":
                    value.connect(
                        "valuechanged",
                        lambda x: GLib.idle_add(lambda: self.set_size(x)),
                    )
                    self.__reload_image()

    def __reload_image(self):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.path)
        pixbuf = pixbuf.scale_simple(
            self.size,
            self.size,
            GdkPixbuf.InterpType.BILINEAR,
        )
        self.set_from_pixbuf(pixbuf)

    def set_path(self, path):
        self.path = path

    def set_size(self, size):
        self.size = size

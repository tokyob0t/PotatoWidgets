from ..Imports import *
from .Common import BasicProps
from ..Variable import Listener, Poll, Variable


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
        css=None,
    ):
        Gtk.Image.__init__(self)
        BasicProps.__init__(
            self,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=False,
            vexpand=False,
            active=True,
            visible=visible,
            classname=classname,
            size=0,
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
                callback = {"path": self.set_path, "size": self.set_size}.get(key)

                self.bind(value, callback) if callback else None

    def __reload_image(self):
        file = Gio.File.new_for_path(self.path)
        if file.query_exists():
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.path)
            pixbuf = pixbuf.scale_simple(
                self.size if isinstance(self.size, (int)) else self.size[0],
                self.size if isinstance(self.size, (int)) else self.size[1],
                GdkPixbuf.InterpType.BILINEAR,
            )
            self.set_from_pixbuf(pixbuf)
            self.show()
        else:
            self.hide()

    def set_path(self, path):
        self.path = path
        self.__reload_image()

    def set_size(self, size):
        self.size = size
        self.__reload_image()

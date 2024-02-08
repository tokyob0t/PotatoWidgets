from typing import Union
from .Common import BasicProps
from ..Variable import Listener, Poll, Variable
from ..Imports import *


class Image(Gtk.Image, BasicProps):
    def __init__(
        self,
        path="",
        size: Union[list, int] = 20,
        halign="fill",
        valign="fill",
        visible=True,
        classname="",
        attributes=lambda self: self,
        css="",
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
            size=size,
        )
        self.size = size
        self.path = path
        self.__reload_image()

        if attributes:
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
                "classname",
            ] and isinstance(value, (Listener, Poll, Variable)):
                callback = {"path": self.set_path, "size": self.set_size}.get(key)
                if callback:
                    self.bind(value, callback)

    def __reload_image(self):
        try:
            file = Gio.File.new_for_path(self.path)
            file_info = file.query_info("*", Gio.FileQueryInfoFlags.NONE, None)
            if file_info.exists():
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.path)
                if isinstance(self.size, int):
                    width = height = self.size
                else:
                    width, height = self.size

                pixbuf = pixbuf.scale_simple(
                    width, height, GdkPixbuf.InterpType.BILINEAR
                )
                self.set_from_pixbuf(pixbuf)
                self.show()
            else:
                self.hide()
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

    def set_path(self, path):
        self.path = path
        self.__reload_image()

    def set_size(self, size):
        self.size = size
        self.__reload_image()

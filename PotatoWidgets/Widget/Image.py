from ..Imports import *
from .Common import BasicProps
from ..Variable import Listener, Poll, Variable


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
    ) -> None:
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

    def __reload_image(self) -> None:
        self.set_from_file(self.path)
        self.set_size(self.size)

    def set_path(self, path) -> None:
        self.path = path
        self.__reload_image()

    def set_size(self, size) -> None:
        self.size = size
        self.__reload_image()

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

        self._path = path
        self._size = size
        self.set_image(self._path, self._size)

        attributes(self) if attributes else None

    def set_size(self, size):
        self._size = size
        self.set_image(self._path, self._size)

    def set_path(self, path):
        self._path = path
        self.set_image(self._path, self._size)

    def set_image(self, path, size):
        size = [size, size] if isinstance(size, (int)) else size

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, size[0], size[1], True)

        self.set_from_pixbuf(pixbuf)
        super().set_size(size)

        self.show()

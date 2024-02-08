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
        self.set_image(path, size)
        attributes(self) if attributes else None

    def set_image(self, path, size):
        size = [size, size] if isinstance(size, (int)) else size

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, size[0], size[1], True)

        self.set_from_pixbuf(pixbuf)

        super().set_size(size)

        self.show()

    def set_size(self, size):
        if isinstance(size, int):
            size = [size, size]
        elif not isinstance(size, list) or len(size) != 2:
            raise ValueError("Size must be an integer or a list of two integers.")
        self.set_image(self.get_path(), size)

    def set_path(self, path):
        self.set_image(path, self.get_size())

    def get_size(self):
        width, height = self.get_pixbuf().get_width(), self.get_pixbuf().get_height()
        return [width, height]

    def get_path(self):
        return self.props.file

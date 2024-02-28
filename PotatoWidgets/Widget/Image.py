from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Image(Gtk.Image, BasicProps):
    def __init__(
        self,
        path="",
        size: Union[list, int] = 20,
        hexpand=False,
        vexpand=False,
        halign="fill",
        valign="fill",
        visible=True,
        classname="",
        attributes: Callable = lambda self: self,
        css="",
    ) -> None:
        Gtk.Image.__init__(self)
        BasicProps.__init__(
            self,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=True,
            visible=visible,
            classname=classname,
            size=0,
        )

        self.set_image(path, size)
        attributes(self) if attributes else None

    def set_image(self, path: str, size: Union[int, List[int]]) -> None:
        size = [size, size] if isinstance(size, (int)) else size

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, size[0], size[1], True)

        self.set_from_pixbuf(pixbuf)

        super().set_size(size)

        self.show()

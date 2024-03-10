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

        self.__size = [0, 0]
        self.__path = ""

        self.set_size(size)
        self.set_image(path)

        attributes(self) if attributes else None

    def set_size(self, size: Union[int, List[int]]) -> None:

        self.__size = [size, size] if isinstance(size, (int)) else size

    def set_image(self, path: str) -> None:
        self.__path = path
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=self.__path,
            width=self.__size[0],
            height=self.__size[1],
            preserve_aspect_ratio=True,
        )

        self.set_from_pixbuf(pixbuf)

        self.show()

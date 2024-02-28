from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Icon(Gtk.Image, BasicProps):
    def __init__(
        self,
        icon: str = "",
        size: int = 20,
        attributes: Callable = lambda self: self,
        css: str = "",
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        visible: bool = True,
        classname: str = "",
    ):
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
        self.__size = size
        self.__icon = icon
        self.set_icon(icon, size)

        attributes(self) if attributes else None

    def set_icon(self, icon: str, size: int) -> None:
        self.__icon = icon
        self.__size = size
        self.set_from_icon_name(self.__icon, Gtk.IconSize.DIALOG)
        self.set_pixel_size(self.__size)

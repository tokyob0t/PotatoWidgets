from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Icon(Gtk.Image, BasicProps):
    def __init__(
        self,
        icon: Union[str, Listener, Poll, Variable] = "",
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
        if isinstance(icon, (Listener, Poll, Variable)):
            self.set_icon(icon.get_value())
        else:
            self.set_icon(icon)

        self.set_size(size)

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
                callback = {
                    "icon": self.set_icon,
                    "size": self.set_size,
                }.get(key)

                if callback:
                    self.bind(value, callback)

        attributes(self) if attributes else None

    def set_icon(self, icon: str) -> None:
        self.__icon = icon
        self.set_from_icon_name(self.__icon, Gtk.IconSize.DIALOG)

    def set_size(self, size: int) -> None:
        self.__size = size
        self.set_pixel_size(self.__size)

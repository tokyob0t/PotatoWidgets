from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Separator(Gtk.Separator, BasicProps):
    def __init__(
        self,
        orientation: str = "h",
        attributes: Callable = lambda self: self,
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        classname: str = "",
        css: str = "",
        size: Union[int, str, List[Union[int, str]], List[int]] = 0,
    ):
        Gtk.Separator.__init__(self)
        BasicProps.__init__(
            self,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=True,
            visible=True,
            classname=classname,
            css=css,
            size=size,
        )
        attributes(self) if attributes else None
        self.set_orientation(orientation)

    def set_orientation(
        self, orientation: Union[Gtk.Orientation, str] = Gtk.Orientation.HORIZONTAL
    ) -> None:
        _orientation = Gtk.Orientation.HORIZONTAL

        if isinstance(orientation, (Gtk.Orientation)):
            _orientation = orientation
        elif orientation == "v":
            _orientation = Gtk.Orientation.VERTICAL
        else:
            _orientation = Gtk.Orientation.HORIZONTAL

        super().set_orientation(_orientation)

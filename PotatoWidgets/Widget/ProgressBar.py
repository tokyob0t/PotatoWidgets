from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class ProgressBar(Gtk.ProgressBar, BasicProps):
    def __init__(
        self,
        value: Union[int, float, Poll, Listener, Variable] = 50,
        showtext: bool = False,
        inverted: bool = False,
        orientation: str = "h",
        attributes: Callable = lambda self: self,
        css: str = "",
        size: Union[int, str, List[Union[int, str]], List[int]] = 0,
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        visible: bool = True,
        classname: str = "",
    ):
        Gtk.ProgressBar.__init__(self)

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
            size=size,
        )
        if isinstance(value, (Variable, Listener, Poll)):
            self.bind(value, self.set_value)
        else:
            self.set_value(value)

        self.set_show_text(showtext)
        self.set_inverted(inverted)
        self.set_orientation(orientation)

        attributes(self) if attributes else None

    def set_value(self, value: Union[int, float]) -> None:
        if 0 <= value <= 100:
            self.set_fraction(value / 100)
            self.set_text(str(value))

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

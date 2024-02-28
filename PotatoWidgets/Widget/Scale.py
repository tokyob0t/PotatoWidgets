from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Scale(Gtk.Scale, BasicProps):
    def __init__(
        self,
        min: int = 0,
        max: int = 100,
        value: int = 50,
        onchange: Union[Callable, None] = None,
        inverted: bool = False,
        draw_value: bool = False,
        decimals: int = 0,
        attributes: Callable = lambda self: self,
        orientation: str = "h",
        css: str = "",
        size: Union[int, str, List[Union[int, str]], List[int]] = [100, 10],
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        visible: bool = True,
        classname: str = "",
    ):
        Gtk.Scale.__init__(self)
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
        self._min = min
        self._max = max
        self._reload_values()
        self.set_value(value)
        self.set_decimals(decimals)
        self.set_inverted(inverted)
        self.set_orientation(orientation)
        self.set_draw_value(draw_value)

        (
            self.connect(
                "value-changed",
                lambda x: onchange(round(x.get_value(), self._decimals)),
            )
            if onchange
            else None
        )

        attributes(self) if attributes else None

    def set_min(self, min: int) -> None:
        self._min = min
        self._reload_values()

    def set_max(self, max: int) -> None:
        self._max = max
        self._reload_values()

    def set_decimals(self, value: int) -> None:
        if value >= 0:
            self._decimals = value
            self.set_digits(value)

    def _reload_values(self) -> None:
        super().set_range(self._min, self._max)

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

from ..Imports import *
from .Common import BasicProps


class Grid(Gtk.Grid, BasicProps):
    def __init__(
        self,
        spacing: Tuple[int, int] = (0, 0),
        size: Union[int, str, List[Union[int, str]], List[int]] = 0,
        attributes: Callable = lambda self: self,
        css: str = "",
        halign: Literal["fill", "start", "center", "end", "baseline"] = "fill",
        valign: Literal["fill", "start", "center", "end", "baseline"] = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        visible: bool = True,
        classname="",
    ) -> None:
        Gtk.Grid.__init__(self)
        BasicProps.__init__(
            self,
            size=size,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=True,
            visible=visible,
            classname=classname,
        )

        attributes(self)

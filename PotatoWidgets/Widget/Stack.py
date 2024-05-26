from PotatoWidgets.Widget.Common.BasicProps import BasicProps

from ..Imports import *
from .Common import BasicProps


class Stack(Gtk.Stack, BasicProps):
    def __init__(
        self,
        children: Dict[str, Gtk.Widget] = {},
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
        Gtk.Stack.__init__(self)

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
        for name, child in children.items():
            self.add_named(child, name)

        attributes(self)

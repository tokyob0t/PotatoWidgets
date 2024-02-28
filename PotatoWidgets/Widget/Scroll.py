from ..Imports import *
from .Common import BasicProps


class Scroll(Gtk.ScrolledWindow, BasicProps):
    def __init__(
        self,
        children: Gtk.Widget,
        attributes: Callable = lambda self: self,
        size: Union[int, str, List[Union[int, str]], List[int]] = 0,
        css: str = "",
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        visible: bool = True,
        classname: str = "",
    ):
        Gtk.ScrolledWindow.__init__(self)
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

        self.add_with_viewport(children) if children else None
        attributes(self)

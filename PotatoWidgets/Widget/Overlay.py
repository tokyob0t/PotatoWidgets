from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Overlay(Gtk.Overlay, BasicProps):
    def __init__(
        self,
        children: List[Gtk.Widget],
        attributes=lambda self: self,
        css: str = "",
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        visible: bool = True,
        classname: str = "",
    ):
        Gtk.Overlay.__init__(self)

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
        )

        self.add(children[0]) if children else None

        if children[1:]:
            for i in children[1:]:
                if i:
                    self.add_overlay(i)

        attributes(self) if attributes else None

from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Button import Button
from .Common import BasicProps


class CheckBox(Gtk.CheckButton, Button):
    def __init__(
        self,
        children: Gtk.Widget,
        onclick: Union[Callable, None] = None,
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        active: bool = True,
        visible: bool = True,
        classname: str = "",
    ):
        super().__init__()

        Button.__init__(
            self,
            children=children,
            onclick=onclick,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=active,
            visible=visible,
            classname=classname,
        )

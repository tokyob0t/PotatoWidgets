from ..Imports import *
from .Common import BasicProps
from ..Variable import Listener, Poll, Variable
from .Button import Button


class CheckBox(Gtk.CheckButton, Button):
    def __init__(
        self,
        children=None,
        onclick=None,
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        active=True,
        visible=True,
        classname="",
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

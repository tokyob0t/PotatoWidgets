from ..Imports import *
from .Common import BasicProps
from ..Variable import Listener, Poll, Variable


class ToggleButton(Gtk.ToggleButton, BasicProps):
    def __init__(
        self,
        children=None,
        onclick=None,
        css="",
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        active=True,
        visible=True,
        classname="",
    ):
        Gtk.ToggleButton.__init__(self)

        BasicProps.__init__(
            self,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=active,
            visible=visible,
            classname=classname,
            css=css,
        )

        self.add(children) if children else None

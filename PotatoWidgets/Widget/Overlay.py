from ..Imports import *
from .Common import BasicProps
from ..Variable import Listener, Poll, Variable


class Overlay(Gtk.Overlay, BasicProps):
    def __init__(
        self,
        children=[],
        attributes=None,
        css=None,
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        visible=True,
        classname="",
    ):
        Gtk.Overlay.__init__(self)

        BasicProps.__init__(
            self,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=None,
            visible=visible,
            classname=classname,
        )

        self.add(children[0]) if children else None
        [self.add_overlay(i) for i in children[1:]] if children else None
        attributes(self) if attributes else None

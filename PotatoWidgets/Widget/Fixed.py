from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Fixed(Gtk.Fixed, BasicProps):
    def __init__(
        self,
        attributes=lambda self: self,
        halign="fill",
        valign="fill",
        classname="",
        css="",
        hexpand=False,
        vexpand=False,
        size=[0],
    ) -> None:
        Gtk.Fixed.__init__(self)
        BasicProps.__init__(
            self,
            active=True,
            visible=True,
            classname=classname,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            size=size,
        )
        attributes(self) if attributes else None

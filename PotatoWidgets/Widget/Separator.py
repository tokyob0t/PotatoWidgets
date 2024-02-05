from ..Imports import *
from .Common import BasicProps
from ..Variable import Listener, Poll, Variable


class Separator(Gtk.Separator, BasicProps):
    def __init__(
        self,
        orientation="h",
        attributes=None,
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        classname="",
        css="",
        size=0,
    ):
        Gtk.Separator.__init__(self, orientation=self.__clasif_orientation(orientation))
        BasicProps.__init__(
            self,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=True,
            visible=True,
            classname=classname,
            css=css,
            size=size,
        )
        attributes(self) if attributes else None

    def set_orientation(self, param):
        return super().set_orientation(self.__clasif_orientation(param))

    def __clasif_orientation(self, orientation):
        if orientation.lower() in ["vertical", "v", 0, False]:
            return Gtk.Orientation.VERTICAL
        elif orientation.lower() in ["horizontal", "h", 1, True]:
            return Gtk.Orientation.HORIZONTAL

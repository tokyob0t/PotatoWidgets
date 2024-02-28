from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class ComboBox(Gtk.ComboBoxText, BasicProps):
    def __init__(
        self,
        children: list = [],
        css: str = "",
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        active: bool = True,
        visible: bool = True,
        classname: str = "",
    ):
        Gtk.ComboBoxText.__init__(self)

        BasicProps.__init__(
            self,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=active,
            visible=visible,
            classname=classname,
        )

        [self.add(i) for i in children if isinstance(i, Gtk.Widget)]
        [self.append_text(i) for i in children if isinstance(i, str)]

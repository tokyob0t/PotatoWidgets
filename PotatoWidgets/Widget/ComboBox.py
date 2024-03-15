from ..Imports import *
from .Common import BasicProps


class ComboBox(Gtk.ComboBoxText, BasicProps):
    def __init__(
        self,
        children: List[Any] = [],
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
        for i in children:
            try:
                self.append_text(str(i))
            except:
                continue

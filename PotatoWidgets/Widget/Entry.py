from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Entry(Gtk.Entry, BasicProps):
    def __init__(
        self,
        placeholder: str = "",
        onchange: Union[Callable, None] = None,
        onenter: Union[Callable, None] = None,
        css: str = "",
        attributes: Callable = lambda self: self,
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        visible: bool = True,
        active: bool = True,
        classname: str = "",
    ):
        Gtk.Entry.__init__(self)
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

        self.set_placeholder_text(placeholder)

        (
            self.connect("changed", lambda _: onchange(self.get_text()))
            if onchange
            else None
        )

        (
            self.connect("activate", lambda _: onenter(self.get_text()))
            if onenter
            else None
        )

        attributes(self) if attributes else None

    def set_placeholder_text(self, text: Any = "") -> None:
        super().set_placeholder_text(str(text))

    def set_text(self, text: Any = "") -> None:
        super().set_text(str(text))

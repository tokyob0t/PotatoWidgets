from ..Imports import *
from .Common import BasicProps
from ..Variable import Listener, Poll, Variable


class Entry(Gtk.Entry, BasicProps):
    def __init__(
        self,
        placeholder="",
        onchange=None,
        onenter=None,
        css="",
        attributes=None,
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        visible=True,
        active=True,
        classname="",
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

        self.connect(
            "changed", lambda _: onchange(self.get_text())
        ) if onchange else None

        self.connect(
            "activate", lambda _: onenter(self.get_text())
        ) if onenter else None

        attributes(self) if attributes else None

    def set_placeholder_text(self, text):
        super().set_placeholder_text(str(text))

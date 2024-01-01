from ..__Import import *
from ._Common._BasicProps import BasicProps


class Entry(Gtk.Entry, BasicProps):
    def __init__(
        self,
        onchange=None,
        onenter=None,
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
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=active,
            visible=visible,
            classname=classname,
        )

        self.connect(
            "changed", lambda _: onchange(self.get_text())
        ) if onchange else None

        self.connect(
            "activate", lambda _: onenter(self.get_text())
        ) if onenter else None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, *args):
        self._value = args

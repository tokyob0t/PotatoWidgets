from ..__Import import *
from ._Common._BasicProps import BasicProps


class Entry(Gtk.Entry, BasicProps):
    def __init__(
        self,
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

        self._value = ""
        # self.connect("insert_at_cursor", self.test)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, *args):
        self._value = args

from ..__Import import *
from ..Variable import Listener, Poll, Variable
from ._Common._BasicProps import BasicProps


class Overlay(Gtk.Overlay, BasicProps):
    def __init__(
        self,
        children=[],
        attributes=lambda self: self,
        css="",
        classname="",
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        visible=True,
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

        self.set_children(children)
        attributes(self)

    def set_children(self, newChildrenList=[]):
        if not newChildrenList:
            return

        for i in self.get_children():
            if i not in newChildrenList:
                i.destroy()
            self.remove(i)

        self.add(newChildrenList[0])
        [self.add_overlay(i) for i in newChildrenList[1:] if i]
        self.show_all()

from ..__Import import *
from ._Common._BasicProps import BasicProps
from ._Common._Events import Events


class EventBox(Gtk.EventBox, Events):
    def __init__(
        self,
        children=None,
        abovechild=False,
        onclick=None,
        onmiddleclick=None,
        onhover=None,
        onhoverlost=None,
        primaryhold=None,
        primaryrelease=None,
        secondaryhold=None,
        secondaryrelease=None,
        attributes=None,
    ):
        Gtk.EventBox.__init__(self)
        Events.__init__(
            self,
            onclick=onclick,
            onmiddleclick=onmiddleclick,
            onhover=onhover,
            onhoverlost=onhoverlost,
            primaryhold=primaryhold,
            primaryrelease=primaryrelease,
            secondaryhold=secondaryhold,
            secondaryrelease=secondaryrelease,
        )

        self.set_above_child(abovechild)
        self.add(children) if children else None
        attributes(self) if attributes else None

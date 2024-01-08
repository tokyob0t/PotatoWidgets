from ..__Import import *
from ._Common._BasicProps import BasicProps
from ._Common._Events import Events


class EventBox(Gtk.EventBox, Events, BasicProps):
    def __init__(
        self,
        children=None,
        onclick=None,
        onmiddleclick=None,
        onhover=None,
        onhoverlost=None,
        onscrollup=None,
        onscrolldown=None,
        primaryhold=None,
        primaryrelease=None,
        secondaryhold=None,
        secondaryrelease=None,
        attributes=None,
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        visible=True,
        classname="",
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

        BasicProps.__init__(
            self,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=None,
            visible=visible,
            classname=classname,
        )
        self.add(children) if children else None

        self.connect("scroll-event", onscrollup)

        attributes(self) if attributes else None

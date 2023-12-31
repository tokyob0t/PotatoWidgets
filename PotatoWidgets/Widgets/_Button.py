from ..__Import import *
from ._Common._BasicProps import BasicProps
from ._Common._Events import Events


class Button(Gtk.Button, BasicProps, Events):
    def __init__(
        self,
        children=None,
        onclick=None,
        onmiddleclick=None,
        onhover=None,
        onhoverlost=None,
        primaryhold=None,
        primaryrelease=None,
        secondaryhold=None,
        secondaryrelease=None,
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        active=True,
        visible=True,
        classname="",
    ):
        Gtk.Button.__init__(self)

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

        self.add(children) if children else None

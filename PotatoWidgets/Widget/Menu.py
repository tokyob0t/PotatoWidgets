from ..Imports import *
from .Common import BasicProps
from ..Variable import Listener, Poll, Variable


class Menu(Gtk.Menu, BasicProps):
    def __init__(
        self,
        children=[],
        css="",
        valign="fill",
        halign="fill",
        hexpand=False,
        vexpand=False,
        classname="",
    ):
        Gtk.Menu.__init__(self)
        BasicProps.__init__(
            self,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            classname=classname,
            active=True,
        )

        [self.append(i) for i in children if children]
        self.show_all()


class MenuItem(Gtk.MenuItem, BasicProps):
    def __init__(
        self,
        children=None,
        submenu=None,
        onactivate=lambda x: x,
        size=[0],
        css="",
        valign="fill",
        halign="fill",
        hexpand=False,
        vexpand=False,
        classname="",
    ):
        Gtk.MenuItem.__init__(self)
        BasicProps.__init__(
            self,
            size=size,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            classname=classname,
            active=True,
        )
        self.add(children) if children else None
        self.set_submenu(submenu) if submenu else None
        self.connect("activate", onactivate) if onactivate else None

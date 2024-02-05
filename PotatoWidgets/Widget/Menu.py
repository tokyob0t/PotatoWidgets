from gi.repository.Gdk import KEY_Amacron
from ..Imports import *
from .Common import BasicProps
from ..Variable import Listener, Poll, Variable


class Menu(Gtk.Menu, BasicProps):
    def __init__(
        self,
        children=[],
        css="",
        size=[0],
        valign="fill",
        halign="fill",
        hexpand=False,
        vexpand=False,
        classname="",
    ):
        Gtk.Menu.__init__(self)
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

        self.connect(
            "activate",
            lambda widget: GLib.idle_add(
                lambda: self.__clasif_args(
                    callback=onactivate,
                    widget=widget,
                    event=False,
                )
            ),
        )

    def __clasif_args(self, widget, event, callback):
        arg_num = callback.__code__.co_argcount
        arg_tuple = callback.__code__.co_varnames[:arg_num]

        if arg_num == 2:
            callback(widget=widget, event=event)

        elif arg_num == 1:
            if "widget" in arg_tuple and widget:
                callback(widget=widget)
            elif "event" in arg_tuple and event:
                callback(event=event)
            else:
                callback(event)
        else:
            callback()

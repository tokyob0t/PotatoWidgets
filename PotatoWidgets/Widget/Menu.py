from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Menu(Gtk.Menu, BasicProps):
    def __init__(
        self,
        children: List[Gtk.MenuItem],
        css: str = "",
        size: Union[int, str, List[Union[int, str]], List[int]] = 0,
        valign: str = "fill",
        halign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        classname: str = "",
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
        children: Gtk.Widget,
        submenu: Union[Gtk.Menu, None] = None,
        onactivate: Callable = lambda callback: callback,
        size: Union[int, str, List[Union[int, str]], List[int]] = 0,
        css: str = "",
        valign: str = "fill",
        halign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        classname: str = "",
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

    def __clasif_args(self, widget, event, callback) -> None:
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

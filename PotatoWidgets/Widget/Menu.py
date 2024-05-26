from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Menu(Gtk.Menu, BasicProps):
    def __init__(
        self,
        children: List[Union[Gtk.MenuItem, Gtk.SeparatorMenuItem]] = [],
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

        for i in children:
            if i:
                self.append(i)

        self.show_all()

    def popup_at_widget(
        self,
        parent_widget: Gtk.Widget,
        trigger_event: Gdk.EventButton,
        parent_anchor: Literal[
            "top", "top_left", "left", "bottom", "bottom_left", "bottom_right"
        ] = "top",
        menu_anchor: Literal[
            "top", "top_left", "left", "bottom", "bottom_left", "bottom_right"
        ] = "top",
    ) -> None:
        _gravity_mapping: Dict[str, Gdk.Gravity] = {
            "top": Gdk.Gravity.NORTH,
            "top_left": Gdk.Gravity.NORTH_WEST,
            "top_right": Gdk.Gravity.NORTH_EAST,
            "left": Gdk.Gravity.WEST,
            "right": Gdk.Gravity.EAST,
            "bottom": Gdk.Gravity.SOUTH,
            "bottom_left": Gdk.Gravity.SOUTH_WEST,
            "bottom_right": Gdk.Gravity.SOUTH_EAST,
        }
        _from = _gravity_mapping.get(parent_anchor, Gdk.Gravity.NORTH)
        _to = _gravity_mapping.get(menu_anchor, Gdk.Gravity.NORTH)

        return super().popup_at_widget(
            widget=parent_widget,
            widget_anchor=_from,
            menu_anchor=_to,
            trigger_event=trigger_event,
        )

    def popup_at_pointer(self, trigger_event: Gdk.EventButton) -> None:
        return super().popup_at_pointer(trigger_event)


class MenuItem(Gtk.MenuItem, BasicProps):
    def __init__(
        self,
        children: Gtk.Widget,
        submenu: Union[Gtk.Menu, None] = None,
        onactivate: Callable = lambda callback: callback,
        size: Union[int, str, List[Union[int, str]], List[int]] = 0,
        halign: Literal["fill", "start", "center", "end", "baseline"] = "fill",
        valign: Literal["fill", "start", "center", "end", "baseline"] = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        classname: str = "",
        css: str = "",
        active: bool = True,
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
            active=active,
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

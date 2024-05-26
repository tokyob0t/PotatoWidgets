from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


# https://lazka.github.io/pgi-docs/Gtk-3.0/classes/FlowBox.html#Gtk.FlowBox.set_activate_on_single_click
class FlowBox(Gtk.FlowBox, BasicProps):
    def __init__(
        self,
        children: List[Union["FlowBoxChild", Gtk.FlowBoxChild]] = [],
        spacing: Tuple[int, int] = (0, 0),
        orientation: Union[
            Gtk.Orientation, Literal["h", "horizontal", "v", "vertical"]
        ] = "h",
        single_click: bool = False,
        halign: Literal["fill", "start", "center", "end", "baseline"] = "fill",
        valign: Literal["fill", "start", "center", "end", "baseline"] = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        classname: str = "",
        css: str = "",
        visible: bool = True,
        active: bool = True,
        size: Union[int, str, List[Union[int, str]], List[int]] = 0,
        attributes: Callable = lambda self: self,
    ) -> None:
        Gtk.FlowBox.__init__(self)
        BasicProps.__init__(
            self,
            halign,
            valign,
            hexpand,
            vexpand,
            classname,
            css,
            visible,
            active,
            size,
            attributes,
        )
        self.set_column_spacing(spacing[0])
        self.set_row_spacing(spacing[1])
        self.set_activate_on_single_click(single_click)
        self.set_orientation(orientation)
        for i in children:
            self.insert(i)

    def set_orientation(
        self,
        orientation: Union[
            Gtk.Orientation, Literal["h", "horizontal", "v", "vertical"]
        ] = Gtk.Orientation.HORIZONTAL,
    ) -> None:

        _orientation: Gtk.Orientation

        if isinstance(orientation, (Gtk.Orientation)):
            _orientation = orientation
        elif orientation in ["h", "horizontal"]:
            _orientation = Gtk.Orientation.HORIZONTAL
        elif orientation in ["v", "vertical"]:
            _orientation = Gtk.Orientation.VERTICAL
        else:
            return

        super().set_orientation(_orientation)

    def set_activate_on_single_click(self, single: bool) -> None:
        return super().set_activate_on_single_click(single)

    def insert(
        self, widget: Union["FlowBoxChild", Gtk.FlowBoxChild], position: int = -1
    ) -> None:
        return super().insert(widget, position)

    def set_max_children_per_line(self, n_children: int) -> None:
        return super().set_max_children_per_line(n_children)

    def set_min_children_per_line(self, n_children: int) -> None:
        return super().set_min_children_per_line(n_children)

    def set_row_spacing(self, spacing: int) -> None:
        return super().set_row_spacing(spacing)

    def set_column_spacing(self, spacing: int) -> None:
        return super().set_column_spacing(spacing)


class FlowBoxChild(Gtk.FlowBoxChild, BasicProps):
    def __init__(
        self,
        onactivate: Callable = lambda *_: _,
        children: Gtk.Widget = Gtk.Box(),
        halign: Literal["fill", "start", "center", "end", "baseline"] = "fill",
        valign: Literal["fill", "start", "center", "end", "baseline"] = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        classname: str = "",
        css: str = "",
        visible: bool = True,
        active: bool = True,
        size: Union[int, str, List[Union[int, str]], List[int]] = 0,
        attributes: Callable = lambda self: self,
    ) -> None:
        Gtk.FlowBoxChild.__init__(self)
        BasicProps.__init__(
            self,
            halign,
            valign,
            hexpand,
            vexpand,
            classname,
            css,
            visible,
            active,
            size,
            attributes,
        )
        self.dict = {"onactivate": onactivate}
        self.add(children)
        self.connect("activate", self.__activate_event)

    def __activate_event(self, widget, event):
        callback = self.dict.get("onactivate")
        if callback:
            self.__clasif_args(widget, event, callback)

    def __clasif_args(self, widget, event, callback: Callable) -> None:
        arg_num = callback.__code__.co_argcount
        arg_tuple = callback.__code__.co_varnames[:arg_num]

        match arg_num:
            case 2:
                callback(widget=widget, event=event)
            case 1:
                if "widget" in arg_tuple and widget:
                    callback(widget=widget)
                elif "event" in arg_tuple and event:
                    callback(event=event)
                else:
                    callback(event)
            case _:
                callback()

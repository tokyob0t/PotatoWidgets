from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Box(Gtk.Box, BasicProps):
    def __init__(
        self,
        children: Union[List[Union[Gtk.Widget, None]], Gtk.Widget, Any] = [],
        orientation: str = "h",
        spacing: int = 0,
        homogeneous: bool = False,
        size: Union[int, str, List[Union[int, str]], List[int]] = 0,
        attributes: Callable = lambda self: self,
        css: str = "",
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        visible: bool = True,
        classname="",
    ) -> None:
        Gtk.Box.__init__(self, spacing=spacing)

        BasicProps.__init__(
            self,
            size=size,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=True,
            visible=visible,
            classname=classname,
        )

        self.set_orientation(orientation)
        self.set_visible(visible)
        self.set_homogeneous(homogeneous) if homogeneous else None
        self.set_children(children)

        attributes(self) if attributes else None

        for key, value in locals().items():
            if key not in [
                "self",
                "halign",
                "valign",
                "hexpand",
                "vexpand",
                "visible",
                "active",
                "visible",
                "classname",
            ] and isinstance(value, (Listener, Poll, Variable)):
                callback = {
                    "orientation": self.set_orientation,
                    "visible": self.set_visible,
                    "spacing": self.set_spacing,
                    "homogeneous": self.set_homogeneous,
                    "children": self.set_children,
                }.get(key)

                self.bind(value, callback) if callback else None

    def set_orientation(
        self, orientation: Union[Gtk.Orientation, str] = Gtk.Orientation.HORIZONTAL
    ) -> None:
        _orientation = Gtk.Orientation.HORIZONTAL

        if isinstance(orientation, (Gtk.Orientation)):
            _orientation = orientation
        elif orientation == "v":
            _orientation = Gtk.Orientation.VERTICAL
        else:
            _orientation = Gtk.Orientation.HORIZONTAL

        super().set_orientation(_orientation)

    def set_children(
        self,
        newChildren: Union[List[Union[Gtk.Widget, None]], Gtk.Widget, Any],
    ) -> None:

        if newChildren is None:
            return

        for children in self.get_children():
            if children not in newChildren:
                children.destroy()
            self.remove(children)

        if isinstance(newChildren, (list)):
            for children in newChildren:
                if isinstance(children, (Gtk.Widget)):
                    self.add(children)

        elif isinstance(newChildren, (Gtk.Widget)):
            self.add(newChildren)

        self.show_all()

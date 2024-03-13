from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Overlay(Gtk.Overlay, BasicProps):
    def __init__(
        self,
        children: Union[List[Union[Gtk.Widget, None]], Any] = [],
        attributes=lambda self: self,
        css: str = "",
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        visible: bool = True,
        classname: str = "",
    ):
        Gtk.Overlay.__init__(self)

        BasicProps.__init__(
            self,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=True,
            visible=visible,
            classname=classname,
        )

        if not children:
            return

        BaseWidget: Union[Gtk.Widget, None] = children.pop(
            children.index(next(i for i in children if isinstance(i, Gtk.Widget)))
        )
        OverlayWidgets: Union[List[None], List[Gtk.Widget]] = [
            i for i in children if isinstance(i, (Gtk.Widget))
        ]

        if BaseWidget:
            self.add(BaseWidget)

        if OverlayWidgets:
            for i in OverlayWidgets:
                self.add_overlay(i)

        attributes(self) if attributes else None

from PotatoWidgets.Methods import parse_interval

from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Revealer(Gtk.Revealer, BasicProps):
    def __init__(
        self,
        children: Gtk.Widget,
        reveal: bool = True,
        transition: str = "crossfade",
        duration: Union[int, str] = 500,
        css: str = "",
        attributes: Callable = lambda self: self,
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        classname: str = "",
    ):
        Gtk.Revealer.__init__(self)

        BasicProps.__init__(
            self,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            classname=classname,
        )
        self.add(children) if children else None
        self.set_duration(duration)
        self.set_transition(transition)
        self.set_revealed(reveal)

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
                    "reveal": self.set_revealed,
                    "transition": self.set_transition,
                    "duration": self.set_duration,
                }.get(key)
                if callback:
                    callback(value.get_value())
                    self.bind(value, callback)

    def set_transition(
        self, transition: Union[str, Gtk.RevealerTransitionType]
    ) -> None:
        if isinstance(transition, (str)):
            anim = {
                "none": Gtk.RevealerTransitionType.NONE,
                "crossfade": Gtk.RevealerTransitionType.CROSSFADE,
                "slideright": Gtk.RevealerTransitionType.SLIDE_RIGHT,
                "slideleft": Gtk.RevealerTransitionType.SLIDE_LEFT,
                "slideright": Gtk.RevealerTransitionType.SLIDE_RIGHT,
                "slideup": Gtk.RevealerTransitionType.SLIDE_UP,
                "slidedown": Gtk.RevealerTransitionType.SLIDE_DOWN,
            }.get(transition.lower(), Gtk.RevealerTransitionType.NONE)
        else:
            anim = transition

        super().set_transition_type(anim)

    def set_duration(self, duration_ms: Union[int, str]) -> None:
        _duration = parse_interval(interval=duration_ms, fallback_interval=500)
        super().set_transition_duration(_duration)

    def set_revealed(self, reveal: bool) -> None:
        super().set_reveal_child(reveal)

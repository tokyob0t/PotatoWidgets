from ..__Import import *
from ..Variable import Listener, Poll, Variable
from ._Common._BasicProps import BasicProps


class Revealer(Gtk.Revealer, BasicProps):
    def __init__(
        self,
        children=None,
        reveal=True,
        transition="crossfade",
        duration=500,
        attributes=None,
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        visible=True,
        classname="",
    ):
        Gtk.Revealer.__init__(self)

        BasicProps.__init__(
            self,
            css=None,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=None,
            visible=visible,
            classname=classname,
            size=None,
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
                    "transition": self.set_revealed,
                    "duration": self.set_transition,
                }.get(key)

                self.bind(value, callback) if callback else None

    def set_transition(self, param):
        super().set_transition_type(self.__clasif_transition(param))

    def set_duration(self, param):
        self.set_transition_duration(param)

    def set_revealed(self, param):
        self.set_reveal_child(param)

    def __clasif_transition(self, param):
        anim = {
            "none": Gtk.RevealerTransitionType.NONE,
            "crossfade": Gtk.RevealerTransitionType.CROSSFADE,
            "slideright": Gtk.RevealerTransitionType.SLIDE_RIGHT,
            "slideleft": Gtk.RevealerTransitionType.SLIDE_LEFT,
            "slideright": Gtk.RevealerTransitionType.SLIDE_RIGHT,
            "slideup": Gtk.RevealerTransitionType.SLIDE_UP,
            "slidedown": Gtk.RevealerTransitionType.SLIDE_DOWN,
        }.get(param.lower(), Gtk.RevealerTransitionType.CROSSFADE)

        return anim

from ..Imports import *
from .Common import BasicProps
from ..Variable import Listener, Poll, Variable


class Label(Gtk.Label, BasicProps):
    def __init__(
        self,
        text="",
        yalign=0.5,
        xalign=0.5,
        angle=0.0,
        maxchars=-1,
        wrap=False,
        attributes=None,
        css=None,
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        visible=True,
        classname="",
        justify="justified",
    ):
        Gtk.Label.__init__(self)
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
        self.set_text(text)
        self.set_yalign(yalign)
        self.set_xalign(xalign)
        self.set_selectable(False)
        self.set_angle(angle)
        self.set_maxchars(maxchars)
        self.set_wrap(wrap)
        self.set_justify(justify)

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
                    "text": self.set_text,
                    "yalign": self.set_yalign,
                    "xalign": self.set_xalign,
                    "angle": self.set_angle,
                    "maxchars": self.set_maxchars,
                    "justify": self.set_justify,
                }.get(key)

                self.bind(value, callback) if callback else None

    def set_text(self, text):
        super().set_text(str(text))

    def set_wrap(self, wrap):
        super().set_line_wrap(wrap)

    def set_maxchars(self, chars):
        if isinstance(chars, (int)) and chars > 0:
            super().set_max_width_chars(chars)
            super().set_ellipsize(Pango.EllipsizeMode.END)

    def set_justify(self, justification):
        if justification == "left":
            super().set_justify(Gtk.Justification.LEFT)
        elif justification == "center":
            super().set_justify(Gtk.Justification.CENTER)
        elif justification == "right":
            super().set_justify(Gtk.Justification.RIGHT)
        elif justification == "justified":
            super().set_justify(Gtk.Justification.FILL)

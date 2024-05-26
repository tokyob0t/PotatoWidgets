from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Label(Gtk.Label, BasicProps):
    def __init__(
        self,
        text: Any = "",
        yalign: float = 0.5,
        xalign: float = 0.5,
        angle: float = 0.0,
        maxchars: int = -1,
        wrap: bool = False,
        attributes: Callable = lambda self: self,
        css: str = "",
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        visible: bool = True,
        classname: str = "",
        justify: str = "justified",
    ) -> None:
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

    def set_text(self, text: Any) -> None:
        return super().set_text(str(text))

    def set_markup(self, text: Any) -> None:
        return super().set_markup(str(text))

    def set_wrap(self, wrap: bool) -> None:
        super().set_line_wrap(wrap)

    def set_maxchars(self, chars: int) -> None:
        if chars > 0:
            super().set_max_width_chars(chars)
            super().set_ellipsize(Pango.EllipsizeMode.END)

    def set_justify(self, jtype: Union[str, Gtk.Justification]) -> None:
        if isinstance(jtype, (str)):
            if jtype == "left":
                super().set_justify(Gtk.Justification.LEFT)
            elif jtype == "center":
                super().set_justify(Gtk.Justification.CENTER)
            elif jtype == "right":
                super().set_justify(Gtk.Justification.RIGHT)
            elif jtype == "justified":
                super().set_justify(Gtk.Justification.FILL)
        else:
            super().set_justify(jtype)

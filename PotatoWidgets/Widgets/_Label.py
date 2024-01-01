from ..__Import import *
from ..Variable import Listener, Poll, Variable
from ._Common._BasicProps import BasicProps


class Label(Gtk.Label, BasicProps):
    def __init__(
        self,
        text,
        yalign=0.5,
        xalign=0.5,
        angle=0.0,
        wrap=False,
        markup=False,
        limit=None,
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        visible=True,
        classname="",
    ):
        Gtk.Label.__init__(self)
        BasicProps.__init__(
            self,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=None,
            visible=visible,
            classname=classname,
        )
        self.set_text(str(text))
        self.set_yalign(yalign)
        self.set_xalign(xalign)
        self.set_selectable(False)
        self.set_line_wrap_mode(wrap)
        self.set_angle(angle)

        self.set_hexpand(True if hexpand else False)
        self.set_vexpand(True if vexpand else False)

        self.set_halign(self.__clasif_halign(halign))
        self.set_valign(self.__clasif_halign(valign))

        self.set_visible(visible)

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
                if key == "text":
                    value.connect("valuechanged", lambda x: self.set_text(str(x)))

                    # value.connect(
                    #    "valuechanged",
                    #    lambda x: GLib.idle_add(lambda: self.set_text(str(x))),
                    # )

    def __clasif_halign(self, param):
        dict = {
            "fill": Gtk.Align.FILL,
            "start": Gtk.Align.START,
            "end": Gtk.Align.END,
            "center": Gtk.Align.CENTER,
            "baseline": Gtk.Align.BASELINE,
        }
        return dict.get(param.lower())

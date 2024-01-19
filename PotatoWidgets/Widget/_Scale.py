from ..__Import import *
from ._Common._BasicProps import BasicProps


class Scale(Gtk.Scale, BasicProps):
    def __init__(
        self,
        min=0,
        max=100,
        value=50,
        onchange=None,
        inverted=False,
        draw_value=False,
        decimals=0,
        attributes=None,
        orientation="h",
        css=None,
        size=[100, 10],
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        visible=True,
        classname="",
    ):
        Gtk.Scale.__init__(self)
        BasicProps.__init__(
            self,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=None,
            visible=visible,
            classname=classname,
            size=size,
        )
        self._min = min
        self._max = max

        self._reload_values()
        self.set_value(value)
        self.set_decimals(decimals)
        self.set_inverted(inverted)
        self.set_orientation(orientation)
        self.set_draw_value(draw_value)

        self.connect(
            "value-changed", lambda x: onchange(x.get_value())
        ) if onchange else None

        attributes(self) if attributes else None

    def set_min(self, min):
        self._min = min
        self._reload_values()

    def set_max(self, max):
        self._max = max
        self._reload_values()

    def set_decimals(self, value):
        self.set_digits(value)

    def _reload_values(self):
        super().set_range(self._min, self._max)

    def set_orientation(self, param):
        return super().set_orientation(self.__clasif_orientation(param))

    def set_children(self, newChildrenList=[]):
        if not newChildrenList:
            return

        for i in self.get_children():
            if i not in newChildrenList:
                i.destroy()
            self.remove(i)

        [self.add(i) for i in newChildrenList]
        self.show_all()

    def __clasif_orientation(self, orientation):
        if orientation.lower() in ["vertical", "v", 0, False]:
            return Gtk.Orientation.VERTICAL
        elif orientation.lower() in ["horizontal", "h", 1, True]:
            return Gtk.Orientation.HORIZONTAL

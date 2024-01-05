from gi.repository import Gtk

from ..__Import import *
from ._Common._BasicProps import BasicProps


class CenterBox(Gtk.Box):
    def __init__(
        self,
        orientation="h",
        start=Gtk.Box(),
        center=Gtk.Box(),
        end=Gtk.Box(),
        classname="",
    ):
        Gtk.Box.__init__(self)
        BasicProps.__init__(
            self,
            halign="fill",
            valign="fill",
            hexpand=False,
            vexpand=False,
            active=None,
            visible=True,
            classname=classname,
        )

        self.__clasif_orientation(orientation)
        self._start_widget = None
        self._center_widget = None
        self._end_widget = None
        self.start_widget = start
        self.center_widget = center
        self.end_widget = end

    def __clasif_orientation(self, orientation):
        if orientation.lower() in ["vertical", "v", 0, False]:
            self.set_orientation(Gtk.Orientation.VERTICAL)
        elif orientation.lower() in ["horizontal", "h", 1, True]:
            self.set_orientation(Gtk.Orientation.HORIZONTAL)

    @property
    def start_widget(self):
        return self._start_widget

    @start_widget.setter
    def start_widget(self, start):
        if self._start_widget:
            self._start_widget.destroy()

        self._set("start-widget", start)
        self._start_widget = start

        if start:
            self.pack_start(start, True, True, 0)

    @property
    def end_widget(self):
        return self._end_widget

    @end_widget.setter
    def end_widget(self, end):
        if self._end_widget:
            self._end_widget.destroy()

        self._set("end-widget", end)
        self._end_widget = end

        if end:
            self.pack_end(end, True, True, 0)

    @property
    def center_widget(self):
        return self._center_widget

    @center_widget.setter
    def center_widget(self, center):
        current_center_widget = self._center_widget

        if not center and current_center_widget:
            current_center_widget.destroy()
            self._center_widget = None
            return

        self.set_center_widget(center)
        self._center_widget = center

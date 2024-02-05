from ..Imports import *
from .Common import BasicProps
from ..Variable import Listener, Poll, Variable
from .Box import Box


class CenterBox(Box):
    def __init__(
        self,
        start=Gtk.Box(),
        center=Gtk.Box(),
        end=Gtk.Box(),
        orientation="h",
        spacing=0,
        homogeneous=False,
        size=[5, 5],
        attributes=None,
        css=None,
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        visible=True,
        classname="",
    ):
        super().__init__(
            orientation=orientation,
            spacing=spacing,
            homogeneous=homogeneous,
            size=size,
            attributes=attributes,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            visible=visible,
            classname=classname,
        )
        self._start_widget = None
        self._center_widget = None
        self._end_widget = None
        self.set_start_widget(start)
        self.set_center_widget(center)
        self.set_end_widget(end)

    def get_start_widget(self):
        return self._start_widget

    def set_start_widget(self, start):
        if self._start_widget:
            self._start_widget.destroy()

        self._start_widget = start

        if start:
            self.pack_start(start, False, False, 0)

    def get_end_widget(self):
        return self._end_widget

    def set_end_widget(self, end):
        if self._end_widget:
            self._end_widget.destroy()

        self._end_widget = end

        if end:
            self.pack_end(self._end_widget, False, False, 0)

    def get_center_widget(self):
        return self._center_widget

    def set_center_widget(self, center):
        if self._center_widget:
            self._center_widget.destroy()
        self._center_widget = center

        super().set_center_widget(center)

from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Box import Box
from .Common import BasicProps


class CenterBox(Box):
    def __init__(
        self,
        start: Gtk.Widget,
        center: Gtk.Widget,
        end: Gtk.Widget,
        orientation: str = "h",
        spacing: int = 0,
        homogeneous: bool = False,
        size: Union[int, str, List[Union[int, str]]] = [5, 5],
        attributes: Callable = lambda self: self,
        css: str = "",
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        visible: bool = True,
        classname: str = "",
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
        self._start_widget = start
        self._center_widget = center
        self._end_widget = end

        self.set_start_widget(start)
        self.set_center_widget(center)
        self.set_end_widget(end)
        self.show_all()
    @property
    def start_widget(self) -> Gtk.Widget:
        return self._start_widget

    @start_widget.setter
    def start_widget(self, start: Gtk.Widget) -> None:
        if self._start_widget:
            self._start_widget.destroy()

        self._start_widget = start

        if start:
            self.pack_start(start, False, False, 0)

    @property
    def end_widget(self) -> Gtk.Widget:
        return self._end_widget

    @end_widget.setter
    def end_widget(self, end: Gtk.Widget) -> None:
        if self._end_widget:
            self._end_widget.destroy()

        self._end_widget = end

        if end:
            self.pack_end(self._end_widget, False, False, 0)

    @property
    def center_widget(self) -> Gtk.Widget:
        return self._center_widget

    @center_widget.setter
    def center_widget(self, center: Gtk.Widget) -> None:
        if self._center_widget:
            self._center_widget.destroy()
        self._center_widget = center

        super().set_center_widget(center)

    def get_start_widget(self) -> Gtk.Widget:
        return self._start_widget

    def set_start_widget(self, start: Gtk.Widget) -> None:
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

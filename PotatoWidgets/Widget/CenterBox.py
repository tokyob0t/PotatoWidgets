from ..Imports import *
from .Box import Box


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
    ) -> None:
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

        self.start_widget = start
        self.center_widget = center
        self.end_widget = end
        # self.show_all()

    @property
    def start_widget(self) -> Union[Gtk.Widget, None]:
        return self._start_widget

    @start_widget.setter
    def start_widget(self, start: Gtk.Widget) -> None:
        if self._start_widget:
            self._start_widget.destroy()

        self._start_widget = start

        if start:
            self.pack_start(start, False, False, 0)

    @property
    def end_widget(self) -> Union[Gtk.Widget, None]:
        return self._end_widget

    @end_widget.setter
    def end_widget(self, end: Gtk.Widget) -> None:
        if self._end_widget:
            self._end_widget.destroy()

        self._end_widget = end

        if end:
            self.pack_end(self._end_widget, False, False, 0)

    @property
    def center_widget(self) -> Union[Gtk.Widget, None]:
        return self._center_widget

    @center_widget.setter
    def center_widget(self, center: Gtk.Widget) -> None:
        if self._center_widget:
            self._center_widget.destroy()
        self._center_widget = center

        super().set_center_widget(center)

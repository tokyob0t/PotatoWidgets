from ..Imports import *
from .Common import BasicProps
from ..Variable import Listener, Poll, Variable
from ..Methods import get_screen_size, parse_screen_size

class Window(Gtk.Window):
    def __init__(
        self,
        size: list=[0, 0],
        at: dict = {},
        position: str = "center",
        layer: str = "top",
        exclusive: Union[bool, int] = False,
        children: Gtk.Widget = Gtk.Box(),
        monitor=0,
        namespace: str = "gtk-layer-shell",
        attributes: Callable = lambda self: self,
        **kwargs,
    ) -> None:
        Gtk.Window.__init__(self)

        self._wayland_display = bool(GLib.getenv("WAYLAND_DISPLAY"))
        self.monitor= monitor
        self.namespace = namespace

        if self._wayland_display:
            GtkLayerShell.init_for_window(self)
            GtkLayerShell.set_namespace(self, self.namespace)

        self.add(children) if children else None
        self.set_layer(layer)
        self.set_size(size)
        self.set_margin(at)
        self.set_exclusive(exclusive)
        self.set_position(position)
        self.hide()
        attributes(self)

    def set_position(self, position: str) -> None:
        position = position.lower()

        if self._wayland_display:
            if position == "center":
                for j in [
                    GtkLayerShell.Edge.TOP,
                    GtkLayerShell.Edge.RIGHT,
                    GtkLayerShell.Edge.LEFT,
                    GtkLayerShell.Edge.BOTTOM,
                ]:
                    GtkLayerShell.set_anchor(self, j, False)
            else:
                for j in position.split(" "):
                    _position = {
                        "top": GtkLayerShell.Edge.TOP,
                        "right": GtkLayerShell.Edge.RIGHT,
                        "left": GtkLayerShell.Edge.LEFT,
                        "bottom": GtkLayerShell.Edge.BOTTOM,
                    }.get(j)

                    if _position:
                        GtkLayerShell.set_anchor(self, _position, True)
        else:
            _size = self.get_size() or [10, 10]

            width, height = get_screen_size(self.monitor)
            width -= _size[0]
            height -= _size[1]

            if position == "center":
                self.move(width // 2, height // 2)
            else:
                for j in position.split(" "):
                    _position = {
                        "top": [width // 2, 0],
                        "bottom": [width // 2, height],
                        "left": [0, height // 2],
                        "right": [width, height // 2],
                    }.get(j)
                    if _position:
                        self.move(_position[0], _position[1])

    def set_margin(self, margins: dict) -> None:
        if self._wayland_display:
            for key, value in margins.items():
                _key = {
                    "top": GtkLayerShell.Edge.TOP,
                    "bottom": GtkLayerShell.Edge.BOTTOM,
                    "left": GtkLayerShell.Edge.LEFT,
                    "right": GtkLayerShell.Edge.RIGHT,
                }.get(key)

                if _key:
                    GtkLayerShell.set_margin(self, _key, value)
        else:
            for key, value in margins.items():
                pass

    def set_exclusive(self, exclusivity: Union[int, bool]) -> None:
        if self._wayland_display:
            if exclusivity == True:
                GtkLayerShell.auto_exclusive_zone_enable(self)
            elif isinstance(exclusivity, int):
                GtkLayerShell.set_exclusive_zone(self, exclusivity)
            else:
                return
        else:
            pass

    def set_layer(self, layer: str) -> None:
        layer = layer.lower()

        if self._wayland_display:
            _layer = {
                "desktop": GtkLayerShell.Layer.BACKGROUND,
                "background": GtkLayerShell.Layer.BACKGROUND,
                "bottom": GtkLayerShell.Layer.BOTTOM,
                "menu": GtkLayerShell.Layer.BOTTOM,
                "dock": GtkLayerShell.Layer.TOP,
                "top": GtkLayerShell.Layer.TOP,
                "popup": GtkLayerShell.Layer.OVERLAY,
                "overlay": GtkLayerShell.Layer.OVERLAY,
            }.get(layer, GtkLayerShell.Layer.TOP)

            GtkLayerShell.set_layer(self, _layer)

        else:
            _layer = {
                "normal": Gdk.WindowTypeHint.NORMAL,
                "dialog": Gdk.WindowTypeHint.DIALOG,
                "tooltip": Gdk.WindowTypeHint.TOOLTIP,
                "notification": Gdk.WindowTypeHint.NOTIFICATION,
                "overlay": Gdk.WindowTypeHint.NOTIFICATION,
                "combo": Gdk.WindowTypeHint.COMBO,
                "dnd": Gdk.WindowTypeHint.DND,
                "bottom": Gdk.WindowTypeHint.MENU,
                "menu": Gdk.WindowTypeHint.MENU,
                "toolbar": Gdk.WindowTypeHint.TOOLBAR,
                "splashscreen": Gdk.WindowTypeHint.SPLASHSCREEN,
                "utility": Gdk.WindowTypeHint.UTILITY,
                "dock": Gdk.WindowTypeHint.DOCK,
                "top": Gdk.WindowTypeHint.DOCK,
                "desktop": Gdk.WindowTypeHint.DESKTOP,
                "background": Gdk.WindowTypeHint.DESKTOP,
                "dropdown": Gdk.WindowTypeHint.DROPDOWN_MENU,
                "popup": Gdk.WindowTypeHint.POPUP_MENU,
            }.get(layer, Gdk.WindowTypeHint.DOCK)

            self.set_type_hint(_layer)

    def set_size(self, size: list) -> None:
        screen = get_screen_size(self.monitor)
        width = parse_screen_size(size[0], screen[0])
        height = parse_screen_size(size[0] if len(size) == 1 else size[1], screen[1])


        self.set_size_request(width, height)

    def bind(self, var:Union[Listener, Variable, Poll], callback:Callable) -> None:
        var.bind(callback)

    def open(self, duration: Union[int, str] = 0) -> None:
        self.show()

        if bool(duration):
            GLib.timeout_add(parse_interval(duration), self.close)

    def close(self) -> None:
        self.hide()

    def toggle(self) -> None:
        if self.get_visible():
            self.close()
        else:
            self.open()

    def __str__(self) -> str:
        return str(self.namespace)

    def __repr__(self) -> str:
        return str(self.namespace)

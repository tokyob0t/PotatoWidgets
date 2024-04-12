from ..Imports import *
from ..Methods import get_screen_size, parse_interval, parse_screen_size
from ..Variable import Listener, Poll, Variable


class Window(Gtk.Window):
    def __init__(
        self,
        size: List[Union[str, int]] = [-1, -1],
        at: dict = {},
        position: str = "center",
        layer: str = "top",
        exclusive: Union[bool, int] = False,
        children: Gtk.Widget = Gtk.Box(),
        focusable: Literal[True, False, "none", "on-demand", "exclusive"] = "none",
        monitor: int = 0,
        namespace: str = "gtk-layer-shell",
        attributes: Callable = lambda self: self,
        disable_layer: bool = False,
    ) -> None:
        Gtk.Window.__init__(self)

        self._wayland_display: bool = bool(GLib.getenv("WAYLAND_DISPLAY"))
        self._disable_layer: bool = disable_layer
        self._monitor: int = monitor

        screen: tuple = get_screen_size(self.monitor)

        _width: int = parse_screen_size(size[0], screen[0])
        _height: int = parse_screen_size(
            size[1] if len(size) >= 2 else size[0], screen[1]
        )
        self._size: List[int] = [max(_width, 1), max(_height, 1)]

        if namespace != "gtk-layer-shell":
            self._name: str = namespace
        else:
            # Hacky Stuff Again
            line: str
            index: int

            _, _, _, line = traceback_extract_stack()[-2]
            index = line.find("=")

            if index != -1:
                self._name: str = line[:index].strip()
            else:
                self._name: str = namespace

        if self._wayland_display and not self._disable_layer:
            GtkLayerShell.init_for_window(self)
            GtkLayerShell.set_namespace(self, self.__name__)
        else:
            self.set_wmclass("potatowindow", "PotatoWindow")
            self.set_app_paintable(True)
            self.set_visual(
                Gdk.Display.get_default().get_default_screen().get_rgba_visual()
            )

            if layer not in ["normal"] and not self._disable_layer:
                self.set_skip_pager_hint(True)
                self.set_skip_taskbar_hint(True)
                self.set_decorated(False)
                self.set_resizable(False)

            if layer in [
                "dock",
                "top",
                "bottom",
                "background",
                "notification",
                "dialog",
            ]:
                self.stick()

            if layer in [
                "dialog",
                "tooltip",
                "notification",
                "combo",
                "dnd",
                "menu",
                "toolbar",
                "dock",
                "splashscreen",
                "utility",
                "dropdown",
                "popup",
                "top",
                "overlay",
            ]:
                self.set_keep_above(True)
            elif layer in [
                "desktop",
                "background",
                "bottom",
            ]:
                self.set_keep_below(True)

        self.add(children) if children else None
        self.set_title(self.__name__)
        self.set_size(size[0], size[1 if len(size) == 2 else 0])
        if self._disable_layer:
            self.set_layer("normal")
        else:
            self.set_layer(layer)

        self.set_position(position)
        self.set_exclusive(exclusive)
        self.set_margin(at)
        self.set_focusable(focusable)
        self.close()
        attributes(self)

    def set_focusable(self, focusable: Union[str, bool]) -> None:
        if self._disable_layer:
            return
        if self._wayland_display:
            _mode = {
                True: GtkLayerShell.KeyboardMode.EXCLUSIVE,
                False: GtkLayerShell.KeyboardMode.NONE,
                "none": GtkLayerShell.KeyboardMode.NONE,
                "on-demand": GtkLayerShell.KeyboardMode.ON_DEMAND,
                "exclusive": GtkLayerShell.KeyboardMode.EXCLUSIVE,
            }.get(focusable, GtkLayerShell.KeyboardMode.NONE)
            GtkLayerShell.set_keyboard_mode(self, _mode)
        else:
            self.set_can_focus(bool(focusable))

    def set_position(self, position: str) -> None:
        if self._disable_layer:
            return
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
                for j in position.split():
                    GtkLayerShell.set_anchor(
                        self,
                        {
                            "top": GtkLayerShell.Edge.TOP,
                            "right": GtkLayerShell.Edge.RIGHT,
                            "left": GtkLayerShell.Edge.LEFT,
                            "bottom": GtkLayerShell.Edge.BOTTOM,
                        }.get(j, GtkLayerShell.Edge.TOP),
                        True,
                    )
        else:
            _size = self.get_size() or [10, 10]

            width, height = get_screen_size(self.monitor)
            width -= _size[0]
            height -= _size[1]

            if position == "center":
                self.move(width // 2, height // 2)
            else:

                if "top" in position:
                    y = 0
                elif "bottom" in position:
                    y = height
                elif "top" in position and "bottom" in position:
                    y = height // 2
                else:
                    y = height // 2

                if "left" in position:
                    x = 0
                elif "right" in position:
                    x = width
                elif "left" in position and "right" in position:
                    x = width // 2
                else:
                    x = width // 2

                self.move(x, y)

    def set_margin(self, margins: dict) -> None:
        if self._disable_layer:
            return

        if self._wayland_display:
            width, height = get_screen_size(self.monitor)

            for key, value in margins.items():
                _key = {
                    "top": GtkLayerShell.Edge.TOP,
                    "bottom": GtkLayerShell.Edge.BOTTOM,
                    "left": GtkLayerShell.Edge.LEFT,
                    "right": GtkLayerShell.Edge.RIGHT,
                }.get(key)

                if _key:
                    if key in ["bottom", "top"]:
                        GtkLayerShell.set_margin(self, _key, value)
                    elif key in ["left", "right"]:
                        value = parse_screen_size(value, width)
                        GtkLayerShell.set_margin(self, _key, value)
        else:
            _size = self.get_size() or [10, 10]

            width, height = get_screen_size(self.monitor)
            width -= _size[0]
            height -= _size[1]

            posx, posy = self.get_position()

            for key, value in margins.items():
                _key = {
                    "top": posy == 0,
                    "bottom": posy == height,
                    "left": posx == 0,
                    "right": posx == width,
                }.get(key)
                if _key:
                    value = parse_screen_size(value, height)

                    if key in ["bottom", "right"]:
                        value = abs(value) * -1

                    if key in ["top", "bottom"]:
                        value = parse_screen_size(value, height)
                        self.move_relative(y=value)
                    elif key in ["left", "right"]:
                        value = parse_screen_size(value, width)
                        self.move_relative(x=value)

    def move_relative(self, x: int = 0, y: int = 0) -> None:
        if self._disable_layer:
            return
        if x != 0:
            _x, _y = self.get_position()
            self.move(_x + x, _y)
        if y != 0:
            _x, _y = self.get_position()
            self.move(_x, _y + y)

    def set_exclusive(self, exclusivity: Union[int, bool]) -> None:

        if self._wayland_display and not self._disable_layer:
            if exclusivity == True:
                GtkLayerShell.auto_exclusive_zone_enable(self)
            elif isinstance(exclusivity, int):
                GtkLayerShell.set_exclusive_zone(self, exclusivity)
            else:
                return
        else:
            pass

    def set_layer(self, layer: str) -> None:
        if self._wayland_display and not self._disable_layer:
            _layer = {
                "background": GtkLayerShell.Layer.BACKGROUND,
                "bottom": GtkLayerShell.Layer.BOTTOM,
                "top": GtkLayerShell.Layer.TOP,
                "overlay": GtkLayerShell.Layer.OVERLAY,
                #
                "desktop": GtkLayerShell.Layer.BACKGROUND,
                "menu": GtkLayerShell.Layer.BOTTOM,
                "dock": GtkLayerShell.Layer.TOP,
                "popup": GtkLayerShell.Layer.OVERLAY,
            }.get(layer, GtkLayerShell.Layer.TOP)

            GtkLayerShell.set_layer(self, _layer)

        else:
            _layer = {
                "normal": Gdk.WindowTypeHint.NORMAL,
                "dialog": Gdk.WindowTypeHint.DIALOG,
                "tooltip": Gdk.WindowTypeHint.TOOLTIP,
                "notification": Gdk.WindowTypeHint.NOTIFICATION,
                "combo": Gdk.WindowTypeHint.COMBO,
                "dnd": Gdk.WindowTypeHint.DND,
                "menu": Gdk.WindowTypeHint.MENU,
                "toolbar": Gdk.WindowTypeHint.TOOLBAR,
                "dock": Gdk.WindowTypeHint.DOCK,
                "splashscreen": Gdk.WindowTypeHint.SPLASHSCREEN,
                "utility": Gdk.WindowTypeHint.UTILITY,
                "desktop": Gdk.WindowTypeHint.DESKTOP,
                "dropdown": Gdk.WindowTypeHint.DROPDOWN_MENU,
                "popup": Gdk.WindowTypeHint.POPUP_MENU,
                #
                "background": Gdk.WindowTypeHint.DESKTOP,
                "bottom": Gdk.WindowTypeHint.DOCK,
                "top": Gdk.WindowTypeHint.DOCK,
                "overlay": Gdk.WindowTypeHint.NOTIFICATION,
            }.get(layer, Gdk.WindowTypeHint.DOCK)

            self.set_type_hint(_layer)

    def set_size(self, width: Union[int, str], height: Union[int, str]) -> None:
        screen = get_screen_size(self.monitor)

        _width = parse_screen_size(width, screen[0])
        _height = parse_screen_size(height, screen[1])

        self._size = [max(_width, 1), max(_height, 1)]

        self.set_default_size(self._size[0], self._size[1])
        self.set_size_request(self._size[0], self._size[1])
        self.resize(self._size[0], self._size[1])

    def bind(self, var: Union[Listener, Variable, Poll], callback: Callable) -> None:
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

    @property
    def monitor(self) -> int:
        return self._monitor

    @property
    def __name__(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self.__name__

    def __repr__(self) -> str:
        return self.__str__()

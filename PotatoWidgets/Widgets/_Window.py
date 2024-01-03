from ..__Import import *

cleantextX = (
    lambda x, perheight: perheight(str(x).replace("%", ""))
    if "%" in str(x)
    else float(str(x).replace("px", ""))
)
cleantextY = (
    lambda x, perwidth: perwidth(str(x).replace("%", ""))
    if "%" in str(x)
    else float(str(x).replace("px", ""))
)


class Window(Gtk.Window):
    def __init__(self, monitor=0, props=None, children=None, parent=None, **kwargs):
        Gtk.Window.__init__(self)
        self.connect("destroy", Gtk.main_quit)
        self.monitor = monitor
        self._screen_width, self._screen_height = self.__calculateResolution(
            self.monitor
        )
        self._perheight = lambda x: (float(x) * self._screen_height) / 100
        self._perwidth = lambda x: (float(x) * self._screen_width) / 100

        self.properties = self.__adjustProps(props)
        self.add(children) if children else None

        # Other settings for the window
        # Useful for popups or something like that
        self.set_title("Potato")
        self.set_destroy_with_parent(True if parent else False)
        self.set_transient_for(parent) if parent else None

        # GtkLayerShell SETTING, etc...
        if not locals().get("disable_gtklayershell", False):
            GtkLayerShell.init_for_window(self)
            GtkLayerShell.set_namespace(
                self, f"potatowindow {self.properties.get('namespace', '')}"
            )
            GtkLayerShell.set_layer(
                self, self.__clasif_layer(self.properties.get("layer", "top"))
            )

        self.__clasif_position(self.properties.get("position", "center"))
        self.__clasif_exclusive(self.properties.get("exclusive", False))
        self.__clasif_at(self.properties.get("at", False))
        self.set_size_request(
            max(self.properties["size"][0], 10), max(self.properties["size"][1], 10)
        )
        self.close()

    def __adjustProps(self, props):
        at = props.get("at", {"top": 0, "bottom": 0, "left": 0, "right": 0})

        at["top"] = cleantextY(at.get("top", 0), self._perwidth)
        at["bottom"] = cleantextY(at.get("bottom", 0), self._perwidth)
        at["left"] = cleantextX(at.get("left", 0), self._perheight)
        at["right"] = cleantextX(at.get("right", 0), self._perheight)

        size = props.get("size", [0, 0])

        props["size"] = [
            cleantextX(size[0], self._perwidth),
            cleantextY(size[1], self._perheight),
        ]
        props["at"] = at

        return props

    def __calculateResolution(self, monitor):
        display = Gdk.Display.get_default()
        n_monitors = display.get_n_monitors()

        if monitor < 0 or monitor >= n_monitors:
            raise ValueError(f"Invalid monitor index: {monitor}")

        monitors = [display.get_monitor(i).get_geometry() for i in range(n_monitors)]
        selected_monitor = monitors[monitor]

        return selected_monitor.width, selected_monitor.height

    def __clasif_layer(self, layer):
        if layer.lower() in ["background", "bg"]:
            return GtkLayerShell.Layer.BACKGROUND
        elif layer.lower() in ["bottom", "bt"]:
            return GtkLayerShell.Layer.BOTTOM
        elif layer.lower() in ["top", "tp"]:
            return GtkLayerShell.Layer.TOP
        elif layer.lower() in ["overlay", "ov"]:
            return GtkLayerShell.Layer.OVERLAY

    def __clasif_position(self, position):
        for i in position.lower().split(" "):
            if i in ["top", "tp"]:
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)

            elif i in ["bottom", "bt"]:
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, True)

            elif i in ["left", "lf"]:
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)

            elif i in ["right", "rg"]:
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, True)

            elif i in ["center", "ct"]:
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, False)
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, False)
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, False)
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, False)

    def __clasif_exclusive(self, exclusivity):
        if exclusivity == True:
            return GtkLayerShell.auto_exclusive_zone_enable(self)
        elif isinstance(exclusivity, int):
            return GtkLayerShell.set_exclusive_zone(self, exclusivity)
        else:
            return

    def __clasif_at(self, at):
        if at:
            for key, value in at.items():
                if key in ["top", "tp"]:
                    GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, value)

                elif key in ["bottom", "bt"]:
                    GtkLayerShell.set_margin(self, GtkLayerShell.Edge.BOTTOM, value)

                elif key in ["left", "lf"]:
                    GtkLayerShell.set_margin(self, GtkLayerShell.Edge.LEFT, value)

                elif key in ["right", "rg"]:
                    GtkLayerShell.set_margin(self, GtkLayerShell.Edge.RIGHT, value)

                elif key in ["center", "ct"]:
                    GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, False)
                    GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, False)
                    GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, False)
                    GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, False)

    # def open(self):
    #   super().open(self)

    # def close(self):
    # super().close(self)

    def open(self):
        self.show()

    def close(self):
        self.hide()

    def toggle(self):
        if self.get_visible():
            self.close()
        else:
            self.open()

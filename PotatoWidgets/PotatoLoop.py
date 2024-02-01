from .__Import import *


class PotatoService(dbus.service.Object):
    def __init__(self, confdir):
        bus_name = dbus.service.BusName(
            "com.T0kyoB0y.PotatoWidgets", bus=dbus.SessionBus()
        )
        super().__init__(bus_name, "/com/T0kyoB0y/PotatoWidgets")

        try:
            sys.path.append(confdir)
            from main import DATA
        except:

            def DATA():
                return {"windows": [], "functions": []}

        self.data = DATA()
        if self.data["windows"]:
            local_vars = inspect.currentframe().f_back.f_locals
            self.data["window_names"] = [
                {"name": self._get_instance_name(i, local_vars), "window": i}
                for i in self.data["windows"]
            ]

    def _get_instance_name(self, instance, local_vars):
        return next((name for name, obj in local_vars.items() if obj is instance), None)

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="", out_signature="s"
    )
    def ListWindows(self):
        return str(
            json.dumps(
                [
                    {
                        "name": self.data["window_names"][i]["name"],
                        "opened": self.data["windows"][i].get_visible(),
                    }
                    for i in range(len(self.data["window_names"]))
                ]
            )
        )

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="", out_signature="s"
    )
    def ListFunctions(self):
        return str(json.dumps([i.__name__ for i in self.data["functions"]]))

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="s", out_signature=""
    )
    def ExecFunction(self, func_name):
        for func in self.data["functions"]:
            if func_name == func.__name__:
                try:
                    func()
                except:
                    return

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="", out_signature="s"
    )
    def ListData(self):
        return str(json.dumps(self.data))

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="ss", out_signature=""
    )
    def WindowAction(self, action, window_name):
        window = next(
            (
                i["window"]
                for i in self.data["window_names"]
                if i["name"] == window_name
            ),
            False,
        )

        if not window:
            return

        if action == "toggle":
            window.toggle()
        elif action == "open":
            window.open()
        if action == "close":
            window.close()


def PotatoLoop(confdir=""):
    try:
        DBusGMainLoop(set_as_default=True)
        PotatoService(confdir)
        Gtk.main()

    except KeyboardInterrupt:
        print("Bye")
        exit(0)

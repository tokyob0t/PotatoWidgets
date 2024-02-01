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
            self.data["windows_name"] = [
                self._Get_instance_name(i) for i in self.data["windows"]
            ]

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="", out_signature="s"
    )
    def ListWindows(self):
        return str(
            json.dumps(
                [
                    {
                        "name": self.data["window_names"][i],
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
        if window_name not in self.data["window_names"]:
            return
        for i in self.data["windows"]:
            if window_name == str(i):
                if action == "toggle":
                    i.toggle()
                elif action == "open":
                    i.open()
                if action == "close":
                    i.close()

    def _Get_instance_name(self, instance):
        for name, obj in inspect.currentframe().f_back.f_locals.items():
            if obj is instance:
                return name
        return None


def PotatoLoop(confdir=""):
    try:
        DBusGMainLoop(set_as_default=True)
        PotatoService(confdir)
        Gtk.main()

    except KeyboardInterrupt:
        print("Bye")
        exit(0)

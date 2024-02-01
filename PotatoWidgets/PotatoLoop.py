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

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="", out_signature="s"
    )
    def ListWindows(self):
        return str(
            json.dumps(
                [
                    {"name": f"{i}", "opened": i.get_visible()}
                    for i in self.data["windows"]
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
        if window_name not in [str(i) for i in self.data["windows"]]:
            return
        for i in self.data["windows"]:
            if window_name == str(i):
                if action == "toggle":
                    i.toggle()
                elif action == "open":
                    i.open()
                if action == "close":
                    i.close()


def PotatoLoop(confdir=""):
    try:
        DBusGMainLoop(set_as_default=True)
        PotatoService(confdir)
        Gtk.main()

    except KeyboardInterrupt:
        print("Bye")
        exit(0)

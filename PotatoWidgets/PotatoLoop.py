from .__Import import *

try:
    sys.path.append(f'{GLib.getenv("HOME")}/.config/potato/')

    from main import DATA
except:
    DATA = lambda: {"windows": []}


class PotatoService(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName(
            "com.T0kyoB0y.PotatoWidgets", bus=dbus.SessionBus()
        )
        super().__init__(bus_name, "/com/T0kyoB0y/PotatoWidgets")

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="", out_signature="s"
    )
    def ListWindows(self):
        return str(
            json.dumps(
                [{"name": f"{i}", "opened": i.get_visible()} for i in DATA()["windows"]]
            )
        )

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="", out_signature="s"
    )
    def ListData(self):
        return str(DATA())

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="ss", out_signature="s"
    )
    def WindowAction(self, action, window_name):
        if window_name not in [str(i) for i in DATA()["windows"]]:
            return f"{window_name} not found"
        for i in DATA()["windows"]:
            if window_name == str(i):
                if action == "toggle":
                    i.toggle()
                elif action == "open":
                    i.open()
                if action == "close":
                    i.close()
                return "success"


def PotatoLoop():
    try:
        DBusGMainLoop(set_as_default=True)
        PotatoService()
        Gtk.main()

    except KeyboardInterrupt:
        print("Bye")
        exit(0)


# if __name__ == "__main__":
#     PotatoLoop()

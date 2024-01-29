from .__Import import *


def is_service_running():
    try:
        bus = dbus.SessionBus()
        obj = bus.get_object(
            "com.T0kyoB0y.PotatoWidgets", "/com/T0kyoB0y/PotatoWidgets"
        )
        _ = dbus.Interface(obj, "com.T0kyoB0y.PotatoWidgets")
        return True
    except dbus.exceptions.DBusException:
        print("PotatoWidgets service is not running.")
        return False


def list_windows():
    if not is_service_running():
        return

    try:
        bus = dbus.SessionBus()
        obj = bus.get_object(
            "com.T0kyoB0y.PotatoWidgets", "/com/T0kyoB0y/PotatoWidgets"
        )
        iface = dbus.Interface(obj, "com.T0kyoB0y.PotatoWidgets")
        windows = json.loads(iface.ListWindows())
        if windows:
            for window in windows:
                if window["opened"]:
                    print("*", end=" ")
                print(window["name"])
    except dbus.exceptions.DBusException as e:
        print(f"Error listing windows: {e}")


def toggle_window(window_name):
    if not is_service_running():
        return

    try:
        bus = dbus.SessionBus()
        obj = bus.get_object(
            "com.T0kyoB0y.PotatoWidgets", "/com/T0kyoB0y/PotatoWidgets"
        )
        iface = dbus.Interface(obj, "com.T0kyoB0y.PotatoWidgets")
        iface.WindowAction("toggle", window_name)
    except dbus.exceptions.DBusException as e:
        print(f"Error toggling window: {e}")


def main():
    parser = argparse.ArgumentParser(description="PotatoWidgets CLI")

    parser.add_argument("--windows", help="List all exported windows")
    parser.add_argument(
        "--toggle", metavar="window", help="Toggle window with the given name"
    )
    args = parser.parse_args()

    if args.windows:
        list_windows()
    elif args.toggle:
        toggle_window(args.toggle)
    else:
        print("Usage: potatocli --help")


if __name__ == "__main__":
    main()

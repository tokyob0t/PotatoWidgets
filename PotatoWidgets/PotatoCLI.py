from .__Import import *


def is_service_running(service_name):
    try:
        bus = dbus.SessionBus()
        obj = bus.get_object(service_name, "/com/T0kyoB0y/PotatoWidgets")
        _ = dbus.Interface(obj, service_name)
        return True
    except dbus.exceptions.DBusException:
        return False


def list_windows():
    if not is_service_running("com.T0kyoB0y.PotatoWidgets"):
        print("PotatoWidgets service is not running.")
        return

    try:
        bus = dbus.SessionBus()
        obj = bus.get_object(
            "com.T0kyoB0y.PotatoWidgets", "/com/T0kyoB0y/PotatoWidgets"
        )
        iface = dbus.Interface(obj, "com.T0kyoB0y.PotatoWidgets")
        windows = iface.ListWindows()
        if windows:
            for window in windows:
                if window["opened"]:
                    print("*", end=" ")
                print(window["name"])
    except dbus.exceptions.DBusException as e:
        print(f"Error listing windows: {e}")


def toggle_window(window_name):
    if not is_service_running("com.T0kyoB0y.PotatoWidgets"):
        print("PotatoWidgets service is not running.")
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

    parser.add_argument(
        "--windows", action="store_true", help="List all exported windows"
    )
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

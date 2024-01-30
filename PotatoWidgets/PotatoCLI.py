from .__Import import *

try:
    bus = dbus.SessionBus()
    obj = bus.get_object("com.T0kyoB0y.PotatoWidgets", "/com/T0kyoB0y/PotatoWidgets")
    iface = dbus.Interface(obj, "com.T0kyoB0y.PotatoWidgets")
except dbus.exceptions.DBusException:
    print("PotatoWidgets service is not running.")
    exit(0)


def list_windows():
    try:
        windows = json.loads(iface.ListWindows())
        if windows:
            for window in windows:
                if window["opened"]:
                    print("*", end=" ")
                print(window["name"])
    except dbus.exceptions.DBusException as e:
        print(f"Error listing windows: {e}")


def list_functions():
    try:
        functions = json.loads(iface.ListFunctions())

        if functions:
            for func in functions:
                print(func)

    except dbus.exceptions.DBusException as e:
        print(f"Error listing windows: {e}")


def exec_function(func_name):
    try:
        iface.WindowAction("toggle", func_name)
    except dbus.exceptions.DBusException as e:
        print(f"Error while executing the callback: {e}")


def window_action(action, window_name):
    try:
        iface.WindowAction(action, window_name)
    except dbus.exceptions.DBusException as e:
        print(f"Error toggling window: {e}")


def main():
    parser = argparse.ArgumentParser(description="PotatoWidgets CLI")

    parser.add_argument(
        "--windows", action="store_true", help="List all exported windows"
    )

    parser.add_argument(
        "--function", action="store_true", help="List all exported functions"
    )
    parser.add_argument(
        "--exec", metavar="function", help="Execute an exported funcion"
    )
    parser.add_argument("--open", metavar="window", help="Open a window")
    parser.add_argument("--close", metavar="window", help="Close a window ")
    parser.add_argument(
        "--toggle", metavar="window", help="Toggle window with the given name"
    )

    args = parser.parse_args()

    if args.windows:
        list_windows()
    elif args.functions:
        list_functions()
    elif args.exec:
        exec_function(args.exec)
    elif args.open:
        window_action("open", args.open)
    elif args.close:
        window_action("close", args.close)
    elif args.toggle:
        window_action("toggle", args.toggle)

    else:
        print("Usage: potatocli --help")


if __name__ == "__main__":
    main()

from ..Imports import *


def connect_to_dbus():
    try:
        session_bus = dbus.SessionBus()
        proxy = session_bus.get_object(
            "com.T0kyoB0y.PotatoWidgets", "/com/T0kyoB0y/PotatoWidgets"
        )
        iface = dbus.Interface(proxy, "com.T0kyoB0y.PotatoWidgets")
        return iface
    except dbus.exceptions.DBusException:
        print("PotatoWidgets service is not running.")
        sys.exit(1)


def list_windows(iface):
    try:
        windows = json.loads(iface.ListWindows())
        if windows:
            for window in windows:
                if window["opened"]:
                    print("*", end=" ")
                print(window["name"])
    except dbus.exceptions.DBusException as e:
        print(f"Error listing windows: {e}")


def list_functions(iface):
    try:
        functions = json.loads(iface.ListFunctions())
        if functions:
            for func in functions:
                print(func)
    except dbus.exceptions.DBusException as e:
        print(f"Error listing functions: {e}")


def exec_function(iface, func_name):
    try:
        iface.ExecFunction(func_name)
    except dbus.exceptions.DBusException as e:
        print(f"Error while executing the callback: {e}")


def window_action(iface, action, window_name):
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
        "--functions", action="store_true", help="List all exported functions"
    )

    parser.add_argument(
        "--exec", metavar="<FUNCTION>", help="Execute an exported function"
    )

    parser.add_argument("--open", metavar="<WINDOW>", help="Open a window")
    parser.add_argument("--close", metavar="<WINDOW>", help="Close a window ")
    parser.add_argument("--toggle", metavar="<WINDOW>", help="Toggle window")

    args = parser.parse_args()

    if args.windows:
        iface = connect_to_dbus()
        list_windows(iface)
    elif args.functions:
        iface = connect_to_dbus()
        list_functions(iface)
    elif args.exec:
        iface = connect_to_dbus()
        exec_function(iface, args.exec)
    elif args.open:
        iface = connect_to_dbus()
        window_action(iface, "open", args.open)
    elif args.close:
        iface = connect_to_dbus()
        window_action(iface, "close", args.close)
    elif args.toggle:
        iface = connect_to_dbus()
        window_action(iface, "toggle", args.toggle)
    else:
        print("Usage: potatocli --help")


if __name__ == "__main__":
    main()

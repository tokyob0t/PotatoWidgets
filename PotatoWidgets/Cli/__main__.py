from ..Imports import *


def get_iface():
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
        windows: List[str] = iface.ListWindows()
        if windows:
            for w in windows:
                print(w)
    except dbus.exceptions.DBusException as e:
        print(f"Error listing windows: {e}")


def list_functions(iface):
    try:
        functions: List[str] = iface.ListFunctions()
        if functions:
            for f in functions:
                print(f)
    except dbus.exceptions.DBusException as e:
        print(f"Error listing functions: {e}")


def exec_function(iface, func_name):
    try:
        out: str = iface.ExecFunction(func_name)
        print(out)

    except dbus.exceptions.DBusException as e:
        print(f"Error while executing the callback: {e}")


def window_action(iface, action, window_name):
    try:
        out: str = iface.WindowAction(action, window_name)
        print(out)
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
        iface = get_iface()
        list_windows(iface)
    elif args.functions:
        iface = get_iface()
        list_functions(iface)
    elif args.exec:
        iface = get_iface()
        exec_function(iface, args.exec)
    elif args.open:
        iface = get_iface()
        window_action(iface, "open", args.open)
    elif args.close:
        iface = get_iface()
        window_action(iface, "close", args.close)
    elif args.toggle:
        iface = get_iface()
        window_action(iface, "toggle", args.toggle)
    else:
        print("Usage: potatocli --help")


if __name__ == "__main__":
    main()

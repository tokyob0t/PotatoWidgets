from ..Imports import *

iface: dbus.Interface
dbusException: type = dbus.exceptions.DBusException


def get_iface():
    global iface
    try:
        session_bus = dbus.SessionBus()
        proxy = session_bus.get_object(
            "com.T0kyoB0y.PotatoWidgets", "/com/T0kyoB0y/PotatoWidgets"
        )
        iface = dbus.Interface(proxy, "com.T0kyoB0y.PotatoWidgets")
        return iface
    except dbusException:
        print("PotatoWidgets service is not running.")
        exit(1)


def list_windows(iface):
    try:
        windows: List[str] = iface.ListWindows()
        if windows:
            for w in windows:
                print(w)
    except dbusException as e:
        print(f"Error listing windows: {e}")


def list_functions(iface):
    try:
        functions: List[str] = iface.ListFunctions()
        if functions:
            for f in functions:
                print(f)
    except dbusException as e:
        print(f"Error listing functions: {e}")


def list_variables(iface):
    try:
        variables: List[str] = iface.ListVariables()
        if variables:
            for v in variables:
                print(v)
    except dbusException as e:
        print(f"Error listing functions: {e}")


def exec_function(iface, func_name):
    try:
        response: str = iface.CallFunction(func_name)
        print(response)

    except dbusException as e:
        print(f"Error while executing the callback: {e}")


def window_action(iface, action, window_name):
    try:
        response: str = iface.WindowAction(action, window_name)
        print(response)
    except dbusException as e:
        print(f"Error toggling window: {e}")


def main():
    global iface
    parser = argparse.ArgumentParser(description="PotatoWidgets CLI")

    args_withoutmetavar: Tuple[List[str], ...] = (
        ["--windows", "List all exported windows"],
        ["--functions", "List all exported functions"],
        ["--variables", "List all exported variables"],
    )

    args_withmetavar: Tuple[List[str], ...] = (
        ["--exec", "<FUNCTION>", "Execute an exported function"],
        ["--open", "<WINDOW>", "Open a window"],
        ["--close", "<WINDOW>", "Close a window"],
        ["--toggle", "<WINDOW>", "Toggle a window"],
    )

    for i in args_withmetavar:
        parser.add_argument(i[0], metavar=i[1], help=i[2])

    for i in args_withoutmetavar:
        parser.add_argument(i[0], action="store_true", help=i[1])

    args = parser.parse_args()

    if not any(
        i
        for i in [
            args.windows,
            args.functions,
            args.variables,
            args.exec,
            args.open,
            args.close,
            args.toggle,
        ]
    ):
        parser.print_help()
        exit(0)

    iface = get_iface()

    if args.windows:
        list_windows(iface)
    elif args.functions:
        list_functions(iface)
    elif args.variables:
        list_variables(iface)
    elif args.exec:
        exec_function(iface, args.exec)
    elif args.open:
        window_action(iface, "open", args.open)
    elif args.close:
        window_action(iface, "close", args.close)
    elif args.toggle:
        window_action(iface, "toggle", args.toggle)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

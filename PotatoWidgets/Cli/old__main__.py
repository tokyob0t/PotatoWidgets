from .. import Bash
from ..Imports import *


def dbuscall(MethodName: str, *args):
    return literal_eval(
        Bash.get_output(
            """gdbus call --session --dest com.T0kyoB0y.PotatoWidgets --object-path /com/T0kyoB0y/PotatoWidgets --method com.T0kyoB0y.PotatoWidgets.{} {} """.format(
                MethodName, " ".join(args)
            )
        )
    )[0]


def list_windows():
    for i in dbuscall("ListWindows"):
        print(i)


def list_functions():
    for i in dbuscall("ListFunctions"):
        print(i)


def list_variables():
    for i in dbuscall("ListVariables"):
        print(i)


def call_function(func_name):
    return print(dbuscall("CallFunction", func_name))


def window_action(action, window_name):
    return print(dbuscall("WindowAction", action, window_name))


def main():
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

    if args.windows:
        list_windows()
    elif args.functions:
        list_functions()
    elif args.variables:
        list_variables()
    elif args.exec:
        call_function(args.exec)
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

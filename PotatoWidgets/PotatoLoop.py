from . import Widget
from .Env import *
from .Imports import *
from .Services import (Applications, NotificationsDbusService,
                       NotificationsService, Style)
from .Variable import Listener, Poll, Variable


class PotatoDbusService(dbus.service.Object):
    def __init__(self, confdir: str):

        bus_name = dbus.service.BusName(
            "com.T0kyoB0y.PotatoWidgets", bus=dbus.SessionBus()
        )
        super().__init__(bus_name, "/com/T0kyoB0y/PotatoWidgets")

        try:
            module_name: str = confdir.split("/").pop(-1)
            init_file: str = confdir + "/" + "__init__.py"

            if dir not in sys.path:
                sys.path.append(confdir)

            spec: Union[ModuleSpec, None] = spec_from_file_location(
                module_name, init_file
            )

            if spec:
                modulo: ModuleType = module_from_spec(spec)
                spec.loader.exec_module(modulo)

                if hasattr(modulo, "DATA"):
                    DATA = modulo.DATA
                else:
                    raise AttributeError
            else:
                raise FileNotFoundError

        except FileNotFoundError:
            print(f"File __init__.py not found in {confdir}")
            DATA = {"windows": [], "functions": [], "variables": []}

        except AttributeError:
            print(f"Error accessing DATA attribute in {confdir}")
            DATA = {"windows": [], "functions": [], "variables": []}

        except Exception as e:
            print(f"Unexpected error in {confdir}: {e}")
            DATA = {"windows": [], "functions": [], "variables": []}

        self.data = {
            "windows": [
                {"name": w.__name__, "window": w}
                for w in DATA.get("windows", [])
                if isinstance(w, (Widget.Window)) and w.__name__
            ],
            "functions": [
                {"name": f.__name__, "function": f}
                for f in DATA.get("functions", [])
                if isinstance(f, (Callable)) and f.__name__ != "<lambda>"
            ],
            "variables": [
                {"name": v.__name__, "variable": v}
                for v in DATA.get("variables", [])
                if isinstance(v, (Variable, Listener, Poll)) and v.__name__
            ],
        }

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="", out_signature="as"
    )
    def ListWindows(self) -> List[str]:
        return [
            ("*" if i["window"].get_visible() else "") + i["name"]
            for i in self.data["windows"]
        ]

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="", out_signature="as"
    )
    def ListFunctions(self) -> List[str]:
        return [i["name"] for i in self.data["functions"]]

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="", out_signature="as"
    )
    def ListVariables(self) -> List[str]:
        return [i["name"] for i in self.data["variables"]]

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="s", out_signature="s"
    )
    def CallFunction(self, callback_name: str) -> str:
        callback: Union[Callable, None] = next(
            (
                i["function"]
                for i in self.data["functions"]
                if i["name"] == callback_name
            ),
            None,
        )
        if callback is not None:
            try:
                callback()
                return "ok"
            except Exception as r:
                return str(r)
        else:
            return "notfound"

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="ss", out_signature="s"
    )
    def WindowAction(self, action: str, window_name: str) -> str:
        window: Union[Widget.Window, None] = next(
            (i["win"] for i in self.data["windows"] if i["name"] == window_name), None
        )

        if window is not None:
            try:
                if action == "toggle":
                    window.toggle()
                elif action == "open":
                    window.open()
                elif action == "close":
                    window.close()
                return "ok"

            except Exception as r:
                return str(r)
        else:
            return "notfound"

    """
    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="sss", out_signature=""
    )
    def UpdateVar(self, var: str, value: str, value_type: str) -> None:
        variable: Union[Variable, Listener, Poll, None] = next(
            (i["var"] for i in self.data["variables"] if i["name"] == var), None
        )
        if variable is not None:
            _type = eval(value_type)
            if _type:
                variable.set_value(_type(value))
    """


def PotatoLoop(confdir: str = DIR_CONFIG_POTATO) -> NoReturn:
    """Starts the Potato application loop and initializes necessary services.

    Args:
        confdir (str): The directory path for configuration. Defaults to DIR_CONFIG_POTATO.

    Returns:
        NoReturn: This function does not return anything.

    Raises:
        KeyboardInterrupt: If the loop is interrupted by a keyboard event.
        Exception: If any other exception occurs during the loop execution.
    """

    if confdir.endswith("/"):
        confdir = confdir[:-1]

    GLibLoop: GLib.MainLoop = GLib.MainLoop()
    ServicesThread: Union[GLib.Thread, None] = None

    def SpawnServices() -> None:
        # Init classes
        Style.load_css(f"{confdir}/style.scss")
        Applications()
        NotificationsService()
        NotificationsDbusService()
        PotatoDbusService(confdir)

    try:
        # Then run the MainLoop
        ServicesThread = GLib.Thread.new(SpawnServices.__name__, SpawnServices)
        # SpawnServices()
        GLibLoop.run()
    except KeyboardInterrupt:
        print("\033[92mBye :)\033[0m")
        GLibLoop.quit()

    except Exception as r:
        print(r)
        GLibLoop.quit()

    finally:
        if ServicesThread is not None:
            ServicesThread.unref()

        exit(0)

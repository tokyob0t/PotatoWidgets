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

            if not spec:
                return

            modulo: ModuleType = module_from_spec(spec)
            spec.loader.exec_module(modulo)

            if hasattr(modulo, "DATA"):
                DATA = modulo.DATA
            else:
                raise AttributeError

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
            """
                Dict[
                    str,
                    List[
                        Dict[str, Union[str, Union[Window, Callable, Variable, Listener, Poll]]]
                    ],
                ]
            """
            "windows": [
                {"name": w.__name__, "win": w}
                for w in DATA.get("windows", [])
                if isinstance(w, (Widget.Window)) and w.__name__
            ],
            "functions": [
                {"name": f.__name__, "func": f}
                for f in DATA.get("functions", [])
                if isinstance(f, (Callable)) and f.__name__ != "<lambda>"
            ],
            "variables": [
                {"name": v.__name__, "var": v}
                for v in DATA.get("variables", [])
                if isinstance(v, (Variable, Listener, Poll)) and v.__name__
            ],
        }

    #
    #
    #   RETURN SOMETHING
    #
    #

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="", out_signature="s"
    )
    def ListWindows(self) -> str:
        return str(
            json.dumps(
                [
                    {"name": i["name"], "opened": i["win"].get_visible()}
                    for i in self.data["windows"]
                ]
            )
        )

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="", out_signature="s"
    )
    def ListFunctions(self) -> str:
        return str(json.dumps([i["name"] for i in self.data["functions"]]))

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="", out_signature="s"
    )
    def ListVariables(self) -> str:
        return str(json.dumps([i["name"] for i in self.data["variables"]]))

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="", out_signature="s"
    )
    def ListData(self) -> str:
        return str(json.dumps(self.data))

    #
    #
    #   NO RETURN
    #
    #

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="s", out_signature=""
    )
    def ExecFunction(self, callback_name: str) -> None:
        callback: Union[Callable, None] = next(
            (i["func"] for i in self.data["functions"] if i["name"] == callback_name),
            None,
        )
        if callback is not None:
            try:
                callback()
            except:
                pass

    @dbus.service.method(
        "com.T0kyoB0y.PotatoWidgets", in_signature="ss", out_signature=""
    )
    def WindowAction(self, action: str, window_name: str) -> None:
        window: Union[Widget.Window, None] = next(
            (i["win"] for i in self.data["windows"] if i["name"] == window_name), None
        )

        if window is not None:
            if action == "toggle":
                window.toggle()
            elif action == "open":
                window.open()
            elif action == "close":
                window.close()
            return

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


def PotatoLoop(confdir: str = DIR_CONFIG_POTATO) -> NoReturn:
    if confdir.endswith("/"):
        confdir = confdir[:-1]

    GLibLoop: GLib.MainLoop = GLib.MainLoop()

    try:
        # Init classes
        PotatoDbusService(confdir)
        Applications()
        NotificationsService()
        NotificationsDbusService()

        Style.load_css(f"{confdir}/style.scss")
        # Then run the MainLoop
        GLibLoop.run()
    except KeyboardInterrupt:
        print("Bye :)")
        GLibLoop.quit()

    except Exception as r:
        print(r)
        GLibLoop.quit()

    finally:
        exit(0)

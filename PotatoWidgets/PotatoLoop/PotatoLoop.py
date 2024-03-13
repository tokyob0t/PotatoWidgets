from PotatoWidgets.Env.Env import DIR_CONFIG_POTATO
from PotatoWidgets.Services.Service import Service

from ..Env import *
from ..Imports import *
from ..Services import (Applications, NotificationsDbusService,
                        NotificationsService, Style)
from ..Variable import Listener, Poll, Variable
from ..Widget import Window


class PotatoDbusService(dbus.service.Object):
    def __init__(self, confdir: str):

        bus_name = dbus.service.BusName(
            "com.T0kyoB0y.PotatoWidgets", bus=dbus.SessionBus()
        )
        super().__init__(bus_name, "/com/T0kyoB0y/PotatoWidgets")

        try:
            sys.path.append(confdir)
            from . import DATA

        except ModuleNotFoundError as r:
            print("Import Error: ")
            print(r)
            DATA = {"windows": [], "functions": [], "variables": []}

        except Exception as r:

            print("Error: ")
            print(r)
            exit(0)

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
                {
                    "name": win.__name__,
                    "win": win,
                }
                for win in DATA["windows"]
                if isinstance(win, (Window)) and win.__name__
            ],
            "functions": [
                {
                    "name": func.__name__,
                    "func": func,
                }
                for func in DATA["functions"]
                if isinstance(func, (Callable)) and func.__name__ != "<lambda>"
            ],
            "variables": [
                {
                    "name": var.__name__,
                    "var": var,
                }
                for var in DATA["variables"]
                if isinstance(var, (Variable, Listener, Poll)) and var.__name__
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
        window: Union[Window, None] = next(
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

    GLibLoop: GLib.MainLoop = GLib.MainLoop()

    try:
        # Init classes
        Applications()
        NotificationsService()
        NotificationsDbusService()
        PotatoDbusService(confdir)

        Style.load_css(
            f"{confdir[:-1] if confdir.endswith('/') else confdir}/style.scss"
        )
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

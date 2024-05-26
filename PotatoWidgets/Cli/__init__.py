from .. import Widget
from .._Logger import Logger
from ..Imports import *
from ..Services.Service import Listener, Poll, Service, Variable

__all__ = ["PotatoService"]

com_T0kyoB0y_PotatoWidgets = """
<?xml version="1.0" encoding="UTF-8"?>
<node>
   <interface name="com.T0kyoB0y.PotatoWidgets">
      <method name="ListWindows">
         <arg name="return" type="as" direction="out" />
      </method>
      <method name="ListFunctions">
         <arg name="return" type="as" direction="out" />
      </method>
      <method name="ListVariables">
         <arg name="return" type="as" direction="out" />
      </method>
      <method name="CallFunction">
         <arg name="callback_name" type="s" direction="in" />
         <arg name="return" type="s" direction="out" />
      </method>
      <method name="WindowAction">
         <arg name="action" type="s" direction="in" />
         <arg name="window_name" type="s" direction="in" />
         <arg name="return" type="s" direction="out" />
      </method>
   </interface>
</node>
"""

NodeInfo = Gio.DBusNodeInfo.new_for_xml(com_T0kyoB0y_PotatoWidgets)


class PotatoService(Service):
    def __init__(self, confdir: str) -> None:
        super().__init__()

        DATA = {"windows": [], "functions": [], "variables": []}
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

        except AttributeError:
            Logger.WARNING(f"DATA variable not found in {confdir}")

        except FileNotFoundError:
            Logger.WARNING(f"File __init__.py not found in {confdir}")

        except Exception as e:
            Logger.ERROR(f"Unexpected error in {confdir}:\n", e)

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

        self.__register__()

    def ListWindows(self) -> GLib.Variant:
        if self.data["windows"]:
            return GLib.Variant(
                "(as)",
                (
                    (
                        f"{'*' if i['window'].get_visible() else ''}{i['name']}"
                        for i in self.data["windows"]
                    ),
                ),
            )

        return GLib.Variant("(as)", (("none",),))

    def ListFunctions(self) -> GLib.Variant:
        if self.data["functions"]:
            return GLib.Variant("(as)", ((i["name"] for i in self.data["functions"]),))
        return GLib.Variant("(as)", (("none",),))

    def ListVariables(self) -> GLib.Variant:
        if self.data["variables"]:
            return GLib.Variant("(as)", ((i["name"] for i in self.data["variables"]),))
        return GLib.Variant("(as)", (("none",),))

    def CallFunction(self, callback_name: str) -> GLib.Variant:
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
                return GLib.Variant("(s)", ("ok",))
            except Exception as r:
                return GLib.Variant("(s)", (str(r),))
        return GLib.Variant("(s)", ("notfound",))

    def WindowAction(self, action: str, window_name: str) -> GLib.Variant:
        window: Union[Widget.Window, None] = next(
            (i["window"] for i in self.data["windows"] if i["name"] == window_name),
            None,
        )
        if not window:
            return GLib.Variant("(s)", ("notfound",))

        try:
            match action:
                case "toggle":
                    window.toggle()
                case "open":
                    window.open()
                case "close":
                    window.close()
                case _:
                    return GLib.Variant("(s)", ("invalid",))
            return GLib.Variant("(s)", ("ok",))
        except:
            return GLib.Variant("(s)", ("error",))

    def __register__(self) -> None:
        Gio.bus_own_name(
            Gio.BusType.SESSION,
            "com.T0kyoB0y.PotatoWidgets",
            Gio.BusNameOwnerFlags.DO_NOT_QUEUE,
            self.__on_success__,
            None,
            self.__on_failed__,
        )

    def __on_success__(
        self,
        Connection: Gio.DBusConnection,
        BusName: Literal["org.freedesktop.Notifications"],
    ):

        Connection.register_object(
            "/com/T0kyoB0y/PotatoWidgets",
            NodeInfo.interfaces[0],
            self.__on_call__,
        )

    def __on_failed__(
        self,
        Connection: Gio.DBusConnection,
        BusName: Literal["org.freedesktop.Notifications"],
    ):
        print("error")

    def __on_call__(
        self,
        Connection: Gio.DBusConnection,
        Sender: str,
        Path: Literal["/org/freedesktop/Notifications"],
        BusName: Literal["org.freedesktop.Notifications"],
        Method: str,
        Parameters: tuple,
        MethodInvocation: Gio.DBusMethodInvocation,
    ):
        # print(Method, Parameters)
        try:
            match Method:
                case "CallFunction":
                    MethodInvocation.return_value(self.CallFunction(*Parameters))
                case "ListWindows":
                    MethodInvocation.return_value(self.ListWindows())
                case "ListFunctions":
                    MethodInvocation.return_value(self.ListFunctions())
                case "ListVariables":
                    MethodInvocation.return_value(self.ListVariables())
                case "WindowAction":
                    MethodInvocation.return_value(self.WindowAction(*Parameters))

        except Exception as r:
            print("ERRORRRRR: ", r)
        finally:
            return Connection.flush()

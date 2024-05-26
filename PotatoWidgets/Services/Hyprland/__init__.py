from ..._Logger import Logger
from ...Bash import Bash
from ...Imports import *
from ..Service import Service


@dataclass
class Client:
    address: str
    mapped: bool
    hidden: bool
    at: Tuple[int, int]
    size: Tuple[int, int]
    workspace: Dict[
        Literal["id", "name"],
        int,
    ]
    floating: bool
    monitor: int
    class_: str
    title: str
    initialClass: str
    initialTitle: str
    pid: int
    xwayland: bool
    pinned: bool
    fullscreen: bool
    fullscreenMode: int
    fakeFullscreen: bool
    grouped: list
    swallowing: str
    focusHistoryID: int


@dataclass
class Workspace:
    id: int
    name: str
    monitor: str
    monitorId: int
    windows: int
    hasfullscreen: bool
    lastwindow: str
    lastwindowtitle: str


@dataclass
class Monitor:
    id: int
    name: str
    x: int
    y: int
    width: int
    height: int
    refreshRate: int
    reserved: Tuple[int, int, int, int]
    focused: bool
    description: str
    # make:str
    # model:str
    # serial:str


# ToDo
class _HyprlandService(Service):
    """
    WIP; PLEASE DONT USE
    """

    # https://wiki.hyprland.org/IPC/#events-list
    __gsignals__ = Service.signals(
        {
            "workspace": [[str]],
            "workspacev2": [[int, str]],
            "focusedmon": [[str, str]],
            "activewindow": [[str, str]],
            "activewindowv2": [[str]],
            # Monitor Things
            "fullscreen": [[bool]],
            "monitorremoved": [[str]],
            "monitoradded": [[str]],
            "monitoraddedv2": [[int, str, str]],
            # Workspace things
            "createworkspace": [[str]],
            "createworkspacev2": [[int, str]],
            "destroyworkspace": [[str]],
            "destroyworkspacev2": [[int, str]],
            "moveworkspace": [[str, str]],
            "moveworkspacev2": [[str, str, str]],
            "renameworkspace": [[str, str]],
            "activespecial": [[str, str]],
            # Windows
            "openwindow": [[str, str, str, str]],
            "closewindow": [[str]],
            "movewindow": [[str, str]],
            "movewindowv2": [[str, str, str]],
            "windowtitle": [[str]],
            "changefloatingmode": [[str, bool]],
            "minimize": [[str, bool]],
            "urgent": [[str]],
            "pin": [[str, bool]],
            # Layers
            "openlayer": [[str]],
            "closelayer": [[str]],
            # Other
            "activelayout": [[str, str]],
            "submap": [[str]],
            "screencast": [[bool, str]],
            "ignoregrouplock": [[bool]],
            "lockgroups": [[bool]],
            "configreloaded": [],
        }
    )
    __gproperties__ = Service.properties(
        {
            "workspaces": [object],
            "monitors": [object],
            "clients": [object],
        }
    )

    def __init__(self) -> None:
        super().__init__()
        self._XDG_RUNTIME_DIR: str = Bash.get_env("XDG_RUNTIME_DIR")
        self._SIGNATURE: str = Bash.get_env("HYPRLAND_INSTANCE_SIGNATURE")
        self._EVENTS_SOCKET: str = (
            f"{self.XDG_RUNTIME_DIR}/hypr/{self.SIGNATURE}/.socket2.sock"
        )
        self._COMMANDS_SOCKET: str = (
            f"{self.XDG_RUNTIME_DIR}/hypr/{self.SIGNATURE}/.socket.sock"
        )

        self._workspaces: List[Workspace] = []
        self._monitors = []
        self._windows = []

        if not self.SIGNATURE:
            return Logger.ERROR("Hyprland Signature not found, is hyprland running?")

        self.__start__()
        for i in self.list_properties():
            self.emit(i)

    def __on_connect(self, client, result, command, callback):
        def wrapper(stream, result, callback):
            data, _ = stream.read_upto_finish(result)
            callback(data)

        connection = client.connect_finish(result)
        output_stream = connection.get_output_stream()
        output_stream.write(command.encode())
        output_stream.flush()

        input_stream = Gio.DataInputStream.new(connection.get_input_stream())
        input_stream.read_upto_async(
            "\x04", -1, GLib.PRIORITY_DEFAULT, None, wrapper, callback
        )

    def hyprctl_async(self, command: str, callback: Callable = lambda _: ()):
        if not self.SIGNATURE:
            return Logger.ERROR("Hyprland Signature not found, is hyprland running?")

        socket_address = Gio.UnixSocketAddress.new(self._COMMANDS_SOCKET)
        socket_client = Gio.SocketClient.new()
        socket_client.connect_async(
            socket_address, None, self.__on_connect, command, callback
        )

    def hyprctl(self, command: str) -> str:
        if not self.SIGNATURE:
            Logger.ERROR("Hyprland Signature not found, is hyprland running?")
            return ""

        socket_address = Gio.UnixSocketAddress.new(self._COMMANDS_SOCKET)
        socket_client = Gio.SocketClient.new()
        connection = socket_client.connect(socket_address)
        output_stream = connection.get_output_stream()
        output_stream.write(command.encode())
        output_stream.flush()

        input_stream = Gio.DataInputStream.new(connection.get_input_stream())
        data, _ = input_stream.read_upto("\x04", -1)
        return data

    def connect(
        self,
        signal_name: Literal[
            "workspace",
            "workspacev2",
            "focusedmon",
            "activewindow",
            "activewindowv2",
            "fullscreen",
            "monitorremoved",
            "monitoradded",
            "monitoraddedv2",
            "createworkspace",
            "createworkspacev2",
            "destroyworkspace",
            "destroyworkspacev2",
            "moveworkspace",
            "moveworkspacev2",
            "renameworkspace",
            "activespecial",
            "openwindow",
            "closewindow",
            "movewindow",
            "movewindowv2",
            "windowtitle",
            "changefloatingmode",
            "minimize",
            "urgent",
            "pin",
            "openlayer",
            "closelayer",
            "activelayout",
            "submap",
            "screencast",
            "ignoregrouplock",
            "lockgroups",
            "configreloaded",
            "workspaces",
            "monitors",
            "clients",
        ],
        callback: Callable,
        *args: Any,
        **kwargs: Any,
    ) -> Union[object, None]:
        return super().connect(signal_name, callback, *args, **kwargs)

    def __start__(self) -> None:
        def wrapper(datainput_stream: Gio.DataInputStream, res: Gio.Task) -> None:
            try:
                signal, data = datainput_stream.read_line_finish_utf8(res)[0].split(
                    ">>"
                )
                self.__handle_data_stream(signal, data)
            except Exception as r:
                Logger.ERROR(r)

            return datainput_stream.read_line_async(
                io_priority=GLib.PRIORITY_LOW, callback=wrapper
            )

        socket_address: Gio.SocketAddress = Gio.UnixSocketAddress.new(
            self.EVENTS_SOCKET
        )
        socket_client: Gio.SocketClient = Gio.SocketClient.new()
        socket_connection: Gio.SocketConnection = socket_client.connect(socket_address)
        datainput_stream: Gio.DataInputStream = Gio.DataInputStream.new(
            socket_connection.get_input_stream()
        )

        return datainput_stream.read_line_async(
            io_priority=GLib.PRIORITY_LOW, callback=wrapper
        )

    @property
    def XDG_RUNTIME_DIR(self) -> str:
        return self._XDG_RUNTIME_DIR

    @property
    def SIGNATURE(self) -> str:
        return self._SIGNATURE

    @property
    def COMMANDS_SOCKET(self) -> str:
        return self._EVENTS_SOCKET

    @property
    def EVENTS_SOCKET(self) -> str:
        return self._EVENTS_SOCKET

    def __handle_data_stream(self, signal: str, args: str) -> None:
        try:
            _args: Union[tuple, list]

            match signal:
                case "workspacev2":
                    _args = args.split(",", 1)
                    _args[0] = int(_args[0])
                case "fullscreen" | "lockgroups" | "ignoregrouplock":
                    _args = args.split(",")
                    _args = [bool(_args[0])]
                case "openwindow":
                    _args = args.split(",", 3)
                case "activewindow":
                    _args = args.split(",", 1)
                case "createworkspacev2" | "destroyworkspacev2":
                    _args = args.split(",", 1)
                    _args[0] = int(_args[0])
                case _:
                    _args = args.split(",")

            # print(signal, ",".join(str(i) for i in _args))
            self.emit(signal, *_args)
        except Exception as e:
            Logger.DEBUG("HyprlandService error, ignore this shit")
            print("------")
            print(e)
            print(f"SIGNAL: {signal}, ARGS: {args}")
            print("------")


HyprlandService = _HyprlandService()

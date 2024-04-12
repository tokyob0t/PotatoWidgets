from .._Logger import Logger
from ..Bash import Bash
from ..Imports import *
from .Service import Service


@dataclass(frozen=True)
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
class HyprlandService(Service):
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
            "destroyworkspacev2": [[str, str]],
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
        self._SIGNATURE: str = Bash.get_env("HYPRLAND_INSTANCE_SIGNATURE")
        self._EVENTS_SOCKET: str = f"/tmp/hypr/{self.SIGNATURE}/.socket2.sock"
        self._COMMANDS_SOCKET: str = f"/tmp/hypr/{self.SIGNATURE}/.socket.sock"
        self.__start__()
        self._workspaces: List[Workspace] = []
        self._monitors = []
        self._windows = []

        for i in self.list_properties():
            self.emit(i)

    def hyprctl(self, cmd, parse_dict: False) -> Union[str, dict]:

        return ""

    def __start__(self) -> None:
        #
        SocketAddress: Gio.SocketAddress
        SocketClient: Gio.SocketClient
        SocketConnection: Gio.SocketConnection
        InputStream: Gio.InputStream
        DataInputStream: Gio.DataInputStream
        EventsSocket: str
        #
        EventsSocket = self.EVENTS_SOCKET

        if not self.SIGNATURE:
            Logger.ERROR("Hyprland Signature not found, is hyprland running?")
            return

        SocketAddress = Gio.UnixSocketAddress.new(EventsSocket)
        SocketClient = Gio.SocketClient.new()
        SocketConnection = SocketClient.connect(SocketAddress)
        InputStream = SocketConnection.get_input_stream()
        DataInputStream = Gio.DataInputStream.new(InputStream)

        DataInputStream.read_line_async(
            io_priority=GLib.PRIORITY_LOW, callback=self.__read_stream
        )

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
        if signal in self.list_signals() + self.list_properties():
            _args: Union[tuple, list]

            match signal:
                case "workspace":
                    _args = args.split(",", 1)
                    _args = [int(_args[0])]
                case "workspacev2":
                    _args = args.split(",", 1)
                    _args = [int(_args[0]), _args[1]]
                case "fullscreen", "lockgroups", "ignoregrouplock":
                    _args = args.split(",")
                    _args = [bool(_args[0])]
                case "openwindow":
                    _args = args.split(",", 3)
                case "activewindow":
                    _args = args.split(",", 1)
                case _:
                    _args = args.split(",")

            # print(signal, ",".join(str(i) for i in _args))
            self.emit(signal, *_args)
        else:
            Logger.DEBUG(f"New signal added, please open a issue on the gh page")
            Logger.DEBUG(signal)

    def __read_stream(self, stream: Gio.DataInputStream, res: Gio.Task) -> None:
        signal: str
        data: str
        output: str

        try:
            output, _ = stream.read_line_finish_utf8(res)
            signal, data = output.split(">>")

            self.__handle_data_stream(signal, data)

        except Exception as r:
            print(r)

        return stream.read_line_async(
            io_priority=GLib.PRIORITY_LOW, callback=self.__read_stream
        )

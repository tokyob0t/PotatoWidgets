from .._Logger import Logger
from ..Bash import Bash
from ..Imports import *
from .Service import Service


# ToDo
class HyprlandService(Service):
    # https://wiki.hyprland.org/IPC/#events-list
    __gsignals__ = Service.signals(
        {
            "workspace": [[int]],
            "workspacev2": [[int, str]],
            "focusedmon": [[str, str]],
            "activewindow": [[str, str]],
            "activewindowv2": [[str]],
            "fullscreen": [[bool]],
            "monitorremoved": [[str]],
            "monitoradded": [[str]],
            "monitoraddedv2": [[str, str, str]],
            "createworkspace": [[str]],
            "destroyworkspace": [[str]],
            "destroyworkspacev2": [[str, str]],
            "moveworkspace": [[str, str]],
            "moveworkspacev2": [[str, str, str]],
            "renameworkspace": [[str, str]],
            "activespecial": [[str, str]],
            "activelayout": [[str, str]],
            "openwindow": [[str, str, str, str]],
            "closewindow": [[str]],
            "movewindow": [[str, str]],
            "movewindowv2": [[str, str, str]],
            "openlayer": [[str]],
            "closelayer": [[str]],
            "submap": [[str]],
            "changefloatingmode": [[str, bool]],
            "urgent": [[str]],
            "minimize": [[str, bool]],
            "screencast": [[bool, str]],
            "windowtitle": [[str]],
            "ignoregrouplock": [[bool]],
            "lockgroups": [[bool]],
            "configreloaded": [],
            "pin": [[str, bool]],
        }
    )
    __gproperties__ = Service.properties(
        {
            "workspaces": [object],
            "monitors": [object],
            "windows": [object],
        }
    )

    def __init__(self) -> None:
        super().__init__()
        self._SIGNATURE: str = Bash.get_env("HYPRLAND_INSTANCE_SIGNATURE")
        self._EVENTS_SOCKET: str = f"/tmp/hypr/{self.SIGNATURE}/.socket2.sock"
        self._COMMANDS_SOCKET: str = f"/tmp/hypr/{self.SIGNATURE}/.socket.sock"
        self.__start__()
        self._workspaces = []
        self._monitors = []
        self._windows = []

        for i in self.list_signals() + self.list_properties():
            self.emit(i)

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

    def __handle_data_stream(self, signal: str, *args) -> None:
        if signal in self.list_signals():
            if "workspace" == signal:
                args = int(args[0])
                args = tuple([args])
            elif "workspacev2" == signal:
                args = int(args[0]), args[1]

            # print(signal, *args)
            self.emit(signal, *args)

            # self.emit(signal, *data.split(","))

    def __read_stream(self, stream: Gio.DataInputStream, res: Gio.Task) -> None:
        signal: str
        data: str
        output: str

        try:
            output, _ = stream.read_line_finish_utf8(res)
            signal, data = output.split(">>")

            self.__handle_data_stream(signal, *tuple(data.split(",")))

        except Exception as r:
            print(r)

        return stream.read_line_async(
            io_priority=GLib.PRIORITY_LOW, callback=self.__read_stream
        )

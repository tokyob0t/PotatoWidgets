from ..Bash import Bash
from ..Imports import *
from .Service import Service


# ToDo
class HyprlandService(Service):
    __gsignals__ = {}

    def __init__(self) -> None:
        super().__init__()
        self._SIGNATURE: str = Bash.get_env("HYPRLAND_INSTANCE_SIGNATURE")
        self._EVENTS_SOCKET: str = f"/tmp/hypr/{self.SIGNATURE}/.socket2.sock"
        self._COMMANDS_SOCKET: str = f"/tmp/hypr/{self.SIGNATURE}/.socket.sock"
        self._start_service(self.EVENTS_SOCKET)

    def _start_service(self, path: str) -> None:
        #
        SocketAddress: Gio.SocketAddress
        SocketClient: Gio.SocketClient
        SocketConnection: Gio.SocketConnection
        InputStream: Gio.InputStream
        DataInputStream: Gio.DataInputStream

        #
        SocketAddress = Gio.UnixSocketAddress.new(path)
        SocketClient = Gio.SocketClient.new()
        SocketConnection = SocketClient.connect(SocketAddress)
        InputStream = SocketConnection.get_input_stream()
        DataInputStream = Gio.DataInputStream.new(InputStream)

        DataInputStream.read_line_async(
            io_priority=GLib.PRIORITY_LOW, callback=self._read_stream
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

    def _handle_data_stream(self, signal, data) -> None:
        print(f"signal: {signal}")
        print(f"data: {data}")
        print()

    def _read_stream(self, stream: Gio.DataInputStream, res: Gio.Task) -> None:
        signal: str
        data: str
        output: str

        try:
            output = stream.read_line_finish_utf8(res)[0]
            signal, data = output.split(">>")
            self._handle_data_stream(signal, data)

        except Exception as r:
            print(r)

        return stream.read_line_async(
            io_priority=GLib.PRIORITY_LOW, callback=self._read_stream
        )

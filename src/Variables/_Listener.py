from subprocess import PIPE, Popen

from ..__Import import *


class Listener(GObject.Object):
    def __init__(self, initial_value, listen_command):
        super().__init__()
        self._value = initial_value
        self._listen_command = listen_command
        self._subprocess = None
        self.start_listen()

    def start_listen(self):
        if not self._listen_command:
            print(f"{self} no tiene un comando de escucha definido")
            return

        if self._subprocess:
            print(f"{self} ya está escuchando")
            return

        cmd = self._listen_command
        if isinstance(cmd, str):
            cmd = [cmd]

        self._subprocess = Popen(cmd, stdout=PIPE, text=True)
        GLib.child_watch_add(self._subprocess.pid, self._on_subprocess_exit)
        GLib.io_add_watch(self._subprocess.stdout, GLib.IO_IN, self._on_stdout_ready)

    def stop_listen(self):
        if self._subprocess:
            self._subprocess.terminate()
            self._subprocess.wait()
            self._subprocess = None
        else:
            print(f"{self} no está escuchando")

    def _on_subprocess_exit(self, pid, condition):
        self._subprocess = None
        print(f"{self} ha dejado de escuchar")
        return False

    def _on_stdout_ready(self, source, condition):
        if condition & GLib.IO_IN:
            output = source.read()
            self.set_value(output.strip())
        return True

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value
        self.notify("value")
        self.emit("changed")

    value = GObject.Property(
        type=str,
        default="",
        flags=GObject.ParamFlags.READWRITE | GObject.ParamFlags.CONSTRUCT,
    )


# WIP

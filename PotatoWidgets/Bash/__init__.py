"""
Utility class for shell-related operations using GLib and Gio libraries.

Methods:
    - expandvars: Expand environment variables and user home directory in a given path.
    - run: Run a command in the shell.
    - get_env: Get the value of an environment variable.
    - get_output: Get the output of a command run in the shell.
    - popen: Open a subprocess to run a command.
    - monitor_file: Monitor changes to a file.
"""

from .._Logger import Logger
from ..Imports import *

__all__ = ["Bash"]


__monitors__ = []

T = TypeVar("T", str, int, dict, float, bool, list, bytes, tuple)


class Bash:
    """
    Utility class for shell-related operations using GLib and Gio libraries.

    Methods:
        - mkdir: Create a directory at the specified path.
        - touch: Create a file at the specified path.
        - cat: Read and return the contents of a file.
        - run: Run a command in the shell (BLOCKING operation).
        - run_async: Run a command in the shell and pass output to a callback (NON-BLOCKING operation).
        - get_output: Run a shell command and return its output (BLOCKING operation).
        - get_output_async: Run a shell command and pass its output to a callback (NON-BLOCKING operation).
        - dir_exists: Check if a directory exists at the specified path.
        - file_exists: Check if a file exists at the specified path.
        - subprocess: Create a new subprocess for running a command.
        - popen: Open a subprocess to run a command, especially useful for executing blocking commands.
        - expandvars: Expand environment variables and user home directory in a given path.
        - monitor_file: Monitor changes to a file.
        - get_env: Get the value of an environment variable.
    """

    @staticmethod
    def dir_exists(path: str) -> bool:
        """
        Check if a directory exists at the specified path.

        Args:
            path (str): The path to the directory.

        Returns:
            bool: True if the directory exists, False otherwise.
        """
        return GLib.file_test(Bash.expandvars(path), GLib.FileTest.IS_DIR)

    @staticmethod
    def file_exists(path: str) -> bool:
        """
        Check if a file exists at the specified path.

        Args:
            path (str): The path to the file.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return GLib.file_test(Bash.expandvars(path), GLib.FileTest.EXISTS)

    @staticmethod
    def mkdir(path: str) -> bool:
        """
        Create a directory at the specified path. By default, parent directories are created if they don't exist.

        Args:
            path (str): The path to the directory.

        Returns:
            bool: True if the directory creation is successful, False otherwise.
        """
        return {0: True, -1: False}.get(
            GLib.mkdir_with_parents(Bash.expandvars(path), 0o755), False
        )

    @staticmethod
    def touch(path: str) -> bool:
        """
        Create a file at the specified path.

        Args:
            path (str): The path to the file.

        Returns:
            bool: True if the file creation is successful, False otherwise.
        """
        return GLib.file_set_contents(filename=Bash.expandvars(path), contents="")

    @staticmethod
    def __to__(
        type: Type[T] = str,
        default: str = "",
    ) -> T:
        if default.endswith("\n"):
            default = default[:-1]

        match type.__name__:
            case "str":
                return str(default)
            case "dict":
                return json.loads(default)
            case "int":
                return int(default)
            case "float":
                return float(default)
            case "list":
                return list(str(default).splitlines())
            case "tuple":
                return tuple(str(default))
            case "bool":
                DictValue = {
                    "[]": False,
                    #
                    "0": False,
                    "1": True,
                    #
                    "yes": True,
                    "no": False,
                    #
                    "true": True,
                    "false": False,
                }.get(default, -1)

                if DictValue == -1:
                    return bool(default)
                else:
                    return DictValue

            case "bytes":
                return str(default).encode()
            case _:
                return str(default)

    @staticmethod
    def cat(
        file_or_path: Union[Gio.File, str],
        to: Type[T] = str,
    ) -> T:
        """
        Read and return the contents of a file. This is a BLOCKING operation.

        Args:
            file_or_path (Union[Gio.File, str]): Either a Gio.File object or the path to the file as a string.

        Returns:
            str: The contents of the file as a string.
        """

        content: bytes

        if not isinstance(file_or_path, (Gio.File)):
            file_or_path = Gio.File.new_for_path(Bash.expandvars(file_or_path))

        _, content, _ = file_or_path.load_contents()
        _content = content.decode()

        return Bash.__to__(to, _content)

    @staticmethod
    def run(cmd: str) -> bool:
        """
        Run a command in the shell.

        This function executes a command in the shell environment. It should be noted that this
        is a BLOCKING operation, meaning that it will halt the main thread until the command completes.

        Args:
            cmd (Union[list, str]): The command to be executed. If a string is provided, it will be parsed as
            a single command. If a list is provided, the elements will be joined with spaces to form a command.

        Returns:
            bool: True if the command ran successfully and returned an exit status of 0, False otherwise.
        """
        proc = Bash.subprocess(cmd)
        proc.communicate()
        return proc.get_successful()

    @staticmethod
    def run_async(cmd: str, callback: Callable = lambda *_: ()) -> None:
        """
        Run a command in the shell.

        This function executes a command in the shell environment and then passes the
        output to the callback.

        NON BLOCKING operation

        Args:
            cmd (Union[list, str]): The command to be executed. If a string is provided, it will be parsed as
            a single command. If a list is provided, the elements will be joined with spaces to form a command.

        Returns:
            bool: True if the command ran successfully and returned an exit status of 0, False otherwise.
        """

        def internal_callback(proc: Gio.Subprocess, res: Gio.Task) -> None:
            nonlocal stderr, stdout
            _, stdout, stderr = proc.communicate_utf8_finish(res)
            if stdout:
                callback(True)
            else:
                callback(False)

        proc: Gio.Subprocess
        stderr: str
        stdout: str

        proc = Bash.subprocess(cmd)
        proc.communicate_utf8_async(callback=internal_callback)

    @staticmethod
    def get_output(
        cmd: str,
        to: Type[T] = str,
    ) -> T:
        """
        Run a shell command and return its output.
        BLOCKING operation.

        Args:
            cmd (str): The command to run.

        Returns:
            str: The output of the command.
        """

        proc: Gio.Subprocess
        stdout: str
        stderr: str

        proc = Bash.subprocess(cmd)

        _, stdout, stderr = proc.communicate_utf8()
        std = stdout or stderr

        return Bash.__to__(to, std)

    @staticmethod
    def get_output_async(
        cmd: str,
        callback: Callable = lambda *_: (),
        to: Type[T] = str,
    ) -> None:
        """
        Run a shell command and pass its output to the callback. NON BLOCKING operation.

        Args:
            cmd (str): The command to run.

        Returns:
            str: The output of the command.
        """

        def internal_callback(proc: Gio.Subprocess, res: Gio.Task) -> None:
            nonlocal stderr, stdout
            _, stdout, stderr = proc.communicate_utf8_finish(res)
            std = stdout or stderr
            callback(Bash.__to__(to, std))

        proc: Gio.Subprocess
        stdout: str
        stderr: str

        proc = Bash.subprocess(cmd)
        proc.communicate_utf8_async(callback=internal_callback)

    @staticmethod
    def subprocess(
        cmd: str,
        stdout_flags: Gio.SubprocessFlags = Gio.SubprocessFlags.STDOUT_PIPE,
        stderr_flags: Gio.SubprocessFlags = Gio.SubprocessFlags.STDERR_PIPE,
    ) -> Gio.Subprocess:

        cmd = Bash.expandvars(cmd)

        return Gio.Subprocess.new(
            argv=["bash", "-c", f"{cmd}"], flags=stdout_flags | stderr_flags
        )

    @staticmethod
    def popen(
        cmd: Union[List[str], str],
        stdout: Union[Callable, None] = None,
        stderr: Union[Callable, None] = None,
    ) -> Union[Gio.Subprocess, None]:
        """
        Open a subprocess to run a command, especially useful for executing blocking commands
        like `pactl subscribe` or `playerctl --follow`.

        Args:
            cmd (Union[List[str], str]): The command to run.
            stdout (Union[Callable, None], optional): Callback function for stdout. Defaults to None.
            stderr (Union[Callable, None], optional): Callback function for stderr. Defaults to None.

        Returns:
            Union[Gio.Subprocess, None]: The subprocess object.

        """
        output: str
        success: bool
        parsed_cmd: List[str]
        proc: Gio.Subprocess
        stdout_stream: Gio.DataInputStream
        stderr_stream: Gio.DataInputStream

        def read_stream(out: Gio.DataInputStream, callback: Callable):
            def internal_callback(stdout: Gio.DataInputStream, res: Gio.Task):
                nonlocal output
                try:
                    output, _ = stdout.read_line_finish_utf8(res)

                    callback(output)

                    return stdout.read_line_async(
                        io_priority=GLib.PRIORITY_LOW, callback=internal_callback
                    )

                except Exception as e:
                    print(e)

            out.read_line_async(
                io_priority=GLib.PRIORITY_LOW, callback=internal_callback
            )

        if isinstance(cmd, (str)):
            cmd = Bash.expandvars(cmd)
            success, parsed_cmd = GLib.shell_parse_argv(cmd)
            if success and parsed_cmd:
                cmd = parsed_cmd

        elif isinstance(cmd, (list)):
            parsed_cmd = [Bash.expandvars(i) for i in cmd]
            if parsed_cmd:
                cmd = parsed_cmd

        if cmd:

            proc = Gio.Subprocess.new(
                argv=cmd,
                flags=Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
            )

            if stdout is not None:
                stdout_stream = Gio.DataInputStream.new(
                    base_stream=proc.get_stdout_pipe()
                )
                read_stream(stdout_stream, stdout)

            if stderr is not None:
                stderr_stream = Gio.DataInputStream.new(
                    base_stream=proc.get_stderr_pipe()
                )
                read_stream(stderr_stream, stderr)

            if stderr is None and stdout is None:
                _ = proc.communicate_async()

            return proc

    @staticmethod
    def expandvars(path: str) -> str:
        """
        Expand environment variables and user home directory in a given path.

        Args:
            path (str): The path containing environment variables and user home directory.

        Returns:
            str: The path with expanded variables and user home directory.
        """

        return os_expanduser(os_expandvars(path))

    @staticmethod
    def monitor_file(
        file_or_path: Union[Gio.File, str],
        flags: Literal[
            "none",
            "send_moved",
            "watch_moves",
            "watch_mounts",
            "hard_links",
        ] = "none",
        callback: Callable = lambda *_: (),
        call_when: List[
            Union[
                Literal["ALL"],
                Literal["changed"],
                Literal["renamed"],
                Literal["moved_in"],
                Literal["moved_out"],
                Literal["deleted"],
                Literal["created"],
                Literal["attribute_changed"],
                Literal["changes_done_hint"],
                Literal["unmounted"],
                Literal["pre_unmount"],
            ],
        ] = ["changed"],
    ) -> Gio.FileMonitor:
        """
        Monitor changes to a file.

        Args:
            file_or_path (Union[Gio.File, str]): Either a Gio.File object or the path to the file to monitor.
            flags (str, optional): Flags to specify monitoring behavior. Defaults to "none".
            callback (Callable, optional): Callback function to be executed when a monitored event occurs. Defaults to lambda *_: ().
            call_when (str, optional): Indicates when the callback will be called depending on the type of event specified.

        Returns:
            None
        """

        monitor: Gio.FileMonitor
        monitor_flags: Gio.FileMonitorFlags
        arg_count: int = callback.__code__.co_argcount

        _call_when: List[Gio.FileMonitorEvent] = []

        _call_when_events: Dict[str, Gio.FileMonitorEvent] = {
            "changed": Gio.FileMonitorEvent.CHANGED,
            "renamed": Gio.FileMonitorEvent.RENAMED,
            "moved_in": Gio.FileMonitorEvent.MOVED_IN,
            "moved_out": Gio.FileMonitorEvent.MOVED_OUT,
            "deleted": Gio.FileMonitorEvent.DELETED,
            "created": Gio.FileMonitorEvent.CREATED,
            "attribute_changed": Gio.FileMonitorEvent.ATTRIBUTE_CHANGED,
            "changes_done_hint": Gio.FileMonitorEvent.CHANGES_DONE_HINT,
            "unmounted": Gio.FileMonitorEvent.UNMOUNTED,
            "pre_unmount": Gio.FileMonitorEvent.PRE_UNMOUNT,
        }

        if isinstance(flags, (str)):
            monitor_flags = {
                "none": Gio.FileMonitorFlags.NONE,
                "send_moved": Gio.FileMonitorFlags.SEND_MOVED,
                "watch_moves": Gio.FileMonitorFlags.WATCH_MOVES,
                "watch_mounts": Gio.FileMonitorFlags.WATCH_MOUNTS,
                "hard_links": Gio.FileMonitorFlags.WATCH_HARD_LINKS,
            }.get(flags, Gio.FileMonitorFlags.NONE)

        if not isinstance(file_or_path, (Gio.File)):
            file_or_path = Gio.File.new_for_path(Bash.expandvars(file_or_path))

        if "ALL" in call_when:
            _call_when = [
                Gio.FileMonitorEvent.PRE_UNMOUNT,
                Gio.FileMonitorEvent.ATTRIBUTE_CHANGED,
                Gio.FileMonitorEvent.CHANGES_DONE_HINT,
                Gio.FileMonitorEvent.MOVED_OUT,
                Gio.FileMonitorEvent.UNMOUNTED,
                Gio.FileMonitorEvent.MOVED_IN,
                Gio.FileMonitorEvent.RENAMED,
                Gio.FileMonitorEvent.CREATED,
                Gio.FileMonitorEvent.DELETED,
                Gio.FileMonitorEvent.CHANGED,
            ]
        else:
            _call_when = list(
                filter(
                    lambda e: e != None,
                    map(_call_when_events.get, call_when),
                )
            )

        def internal_callback(
            FileMonitor: Gio.FileMonitor,
            File: Gio.File,
            _: None,
            Event: Gio.FileMonitorEvent,
        ) -> None:

            if Event in _call_when:
                match arg_count:
                    case 0:
                        callback()
                    case 1:
                        callback(File)
                    case 2:
                        callback(File, Event)
                    case _:
                        callback(File, Event, FileMonitor)

        monitor = file_or_path.monitor(flags=monitor_flags)
        __monitors__.append(monitor)

        monitor.connect("notify::cancelled", lambda _: __monitors__.remove(monitor))
        monitor.connect("changed", internal_callback)
        return monitor

    @staticmethod
    def get_env(var: str) -> str:
        """
        Get the value of an environment variable.

        Args:
            var (str): The name of the environment variable.

        Returns:
            str: The value of the environment variable.
        """
        return GLib.getenv(var)

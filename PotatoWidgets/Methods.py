from .Imports import *


def parse_interval(
    interval: Union[int, str] = 1000, fallback_interval: int = 1000
) -> int:
    """Parse the interval in milliseconds.

    Args:
        interval (Union[int, str], optional): The interval to parse, can be in milliseconds (int)
            or in string format indicating seconds ('s'), minutes ('m'), or hours ('h').
            Defaults to 1000 (1 second).

    Returns:
        int: The parsed interval in milliseconds.
    """
    try:
        if isinstance(interval, str):
            unit = interval[-1].lower()
            value = int(interval[:-1])

            if unit == "s":
                return int(value * 1000)
            elif unit == "m":
                return int(value * 60 * 1000)
            elif unit == "h":
                return int(value * 60 * 60 * 1000)
        else:
            return int(interval)

    except (ValueError, IndexError):
        pass

    return fallback_interval


def get_screen_size(
    monitor_index: int = 0, fallback_size: tuple = (1920, 1080)
) -> tuple:
    """Get the screen size.

    Args:
        monitor_index (int, optional): The index of the monitor to get the size of. Defaults to 0.
        fallback_size (tuple, optional): A tuple containing the width and height to return
            if the display is not available or the monitor index is out of range.
            Defaults to (1920, 1080).

    Returns:
        tuple: A tuple containing the width and height of the specified monitor,
            or the fallback size if the display is not available or the index is out of range.
    """
    display = Gdk.Display.get_default()
    if display and 0 <= monitor_index < display.get_n_monitors():
        monitor = display.get_monitor(monitor_index)
        geometry = monitor.get_geometry()
        if geometry:
            return geometry.width, geometry.height
        else:
            return fallback_size
    else:
        return fallback_size


def parse_screen_size(value: Union[int, str], total: int = 0) -> int:
    """Parse the screen size.

    Args:
        value (Union[int, str, bool]): The screen size value, which can be a string with percentage,
            an integer, or a boolean.
        total (int, optional): Total value. Defaults to 0.

    Returns:
        int: The parsed screen size.
    """
    if isinstance(value, str) and "%" in value:
        percentage = float(value.strip("%")) / 100
        return int(total * percentage)
    elif isinstance(value, (int, float)):
        return int(value)
    else:
        return 10


def wait(time_ms: Union[str, int], callback: Callable) -> int:
    """Wait for a specified amount of time and then execute a callback function.

    Args:
        time_ms (Union[str, int]): The time to wait before executing the callback.
        callback (Callable): The function to call after the specified time has elapsed.
    """

    def on_timeout() -> bool:
        callback()
        return False

    return GLib.timeout_add(parse_interval(time_ms), on_timeout)


def lookup_icon(
    icon_name: str,
    size: Literal[8, 16, 32, 64, 128] = 128,
    path: bool = True,
    fallback: str = "application-x-addon-symbolic",
) -> str:
    """Look up an icon by name and return its file path or icon info.

    Args:
        icon_name (str): The name of the icon to look up.
        size (Literal[8, 16, 32, 64, 128], optional): The size of the icon. Defaults to 128.
        path (bool, optional): Whether to return the file path of the icon. Defaults to True.
        fallback (str, optional): The name of the icon to use if the specified icon is not found.
            Defaults to "application-x-addon-symbolic".

    Returns:
        str: The file path of the icon if path=True, otherwise the icon info.
    """
    if icon_name is not None:
        theme = Gtk.IconTheme.get_default()

        for name in [
            icon_name,
            icon_name.lower(),
            icon_name.title(),
            icon_name.capitalize(),
        ]:
            icon_info = theme.lookup_icon(
                name,
                size,
                Gtk.IconLookupFlags.USE_BUILTIN,
            )
            if icon_info is not None:
                return icon_info.get_filename() if path else icon_info

    return lookup_icon(fallback) if path else lookup_icon(fallback, path=False)


def getoutput(cmd: str) -> str:
    """Execute a command and return its output or error message.

    Args:
        cmd (str): The command to execute.

    Returns:
        str: The output of the command if successful, otherwise an empty string.
    """
    stdout: bytes
    stderr: bytes
    state: int

    try:
        _, stdout, stderr, state = GLib.spawn_command_line_sync(cmd)
        print(
            f"getoutput Method is deprecated, use Bash.get_output() instead, out= {stdout.decode()}"
        )
        return stdout.decode() if state == 0 else stderr.decode()
    except GLib.Error:
        return ""


class Bash:
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
    def get_env(var: str) -> str:
        """
        Get the value of an environment variable.

        Args:
            var (str): The name of the environment variable.

        Returns:
            str: The value of the environment variable.

        """
        return GLib.getenv(variable=var)

    @staticmethod
    def run(cmd: Union[List[str], str]) -> int:
        """
        Run a command in the shell.

        Args:
            cmd (Union[List[str], str]): The command to run.

        Returns:
            int: The exit status of the command.

        """
        state: int
        if isinstance(cmd, (list)):
            cmd = [Bash.expandvars(i) for i in cmd]
        elif isinstance(cmd, (str)):
            cmd = Bash.expandvars(cmd)

        try:
            _, _, _, state = GLib.spawn_command_line_sync(cmd)
            return state
        except:
            return -1

    @staticmethod
    def get_output(cmd: str) -> str:
        """
        Get the output of a command run in the shell.

        Args:
            cmd (str): The command to run.

        Returns:
            str: The output of the command.

        """
        stdout: bytes
        stderr: bytes
        state: int

        cmd = Bash.expandvars(cmd)

        try:
            _, stdout, stderr, state = GLib.spawn_command_line_sync(cmd)
            return stdout.decode() if state == 0 else stderr.decode()
        except:
            return ""

    @staticmethod
    def monitor_file(path: str, flags):
        """
        Monitor changes to a file.

        Args:
            path (str): The path to the file to monitor.
            flags: Flags to specify monitoring behavior.

        Returns:
            Gio.FileMonitor: The file monitor object.

        """
        file: Gio.File
        monitor: Gio.FileMonitor
        file = Gio.File.new_for_path(path)
        monitor = file.monitor(flags=Gio.FileMonitorFlags.NONE)
        return monitor

    @staticmethod
    def popen(
        cmd: Union[List[str], str],
        stdout: Union[Callable, None] = None,
        stderr: Union[Callable, None] = None,
    ) -> Union[Gio.Subprocess, None]:
        """
        Open a subprocess to run a command.

        Args:
            cmd (Union[List[str], str]): The command to run.
            stdout (Union[Callable, None], optional): Callback function for stdout. Defaults to None.
            stderr (Union[Callable, None], optional): Callback function for stderr. Defaults to None.

        Returns:
            Union[Gio.Subprocess, None]: The subprocess object.

        """
        output: str
        success: bool
        argv: List[str]
        proc: Gio.Subprocess
        stdout_pipe: Gio.InputStream
        stderr_pipe: Gio.InputStream
        stdout_stream: Gio.DataInputStream
        stderr_stream: Gio.DataInputStream

        def read_stream(out: Gio.DataInputStream, callback: Callable):
            def internal_callback(stdout: Gio.DataInputStream, res: Gio.Task):
                nonlocal output
                try:
                    output = stdout.read_line_finish_utf8(res)[0]
                    return (
                        callback(output),
                        stdout.read_line_async(
                            io_priority=GLib.PRIORITY_LOW, callback=internal_callback
                        ),
                    )
                except Exception as e:
                    print(e)

            out.read_line_async(
                io_priority=GLib.PRIORITY_LOW, callback=internal_callback
            )

        if isinstance(cmd, str):
            success, argv = GLib.shell_parse_argv(cmd)
            if success and argv:
                cmd = argv

        if cmd:

            proc = Gio.Subprocess.new(
                argv=cmd,
                flags=Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
            )

            if stdout is not None:
                stdout_pipe = proc.get_stdout_pipe()
                stdout_stream = Gio.DataInputStream.new(base_stream=stdout_pipe)
                read_stream(stdout_stream, stdout)

            if stderr is not None:
                stderr_pipe = proc.get_stderr_pipe()
                stderr_stream = Gio.DataInputStream.new(base_stream=stderr_pipe)
                read_stream(stderr_stream, stderr)

            return proc

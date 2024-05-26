"""
This module provides utility functions for parsing intervals, getting screen sizes,
waiting for timeouts, scheduling idle callbacks, looking up icons, and executing commands.

    wait: Waits for a specified time and executes a callback function.
    interval: Sets up recurring intervals to execute a callback function.
    idle: Schedules a callback function to be executed when the main event loop is idle.
    lookup_icon: Looks up icons by name and returns file paths or icon information.
    getoutput: Executes a command and returns its output or error message.
    parse_interval: Parses intervals in milliseconds or seconds/minutes/hours.
    get_screen_size: Retrieves the screen size of a specified monitor.
    parse_screen_size: Parses screen size values (percentage, integer, or boolean).

Note: The getoutput method is deprecated and recommended to use Bash.get_output() instead.
"""

from ..Imports import *

__all__ = [
    "get_screen_size",
    "getoutput",
    "idle",
    "interval",
    "lookup_icon",
    "parse_interval",
    "parse_screen_size",
    "wait",
    "make_async",
]


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
    unit: str
    value: int
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
    monitor_index: int = 0, fallback_size: Tuple[int, int] = (1920, 1080)
) -> Tuple[int, int]:
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
    display: Gdk.Display
    monitor: Gdk.Monitor
    geometry: Gdk.Rectangle

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


def wait(
    time_ms: Union[str, int], callback: Callable, *args: Any, **kwargs: Any
) -> int:
    """Wait for a specified amount of time and then execute a callback function.

    Args:
        time_ms (Union[str, int]): The time to wait before executing the callback.
        callback (Callable): The function to call after the specified time has elapsed.

    Returns:
        int: The ID of the timeout source.
    """

    def on_timeout() -> bool:
        callback(*args, **kwargs)
        return False

    return GLib.timeout_add(parse_interval(time_ms), on_timeout)


def interval(
    time_ms: Union[str, int], callback: Callable, *args: Any, **kwargs: Any
) -> int:
    """Sets a function to be called at regular intervals.

    Args:
        time_ms (Union[str, int]): The interval between callback executions.
        callback (Callable): The function to call at each interval.

    Returns:
        int: The ID of the timeout source.
    """

    def on_timeout() -> bool:
        callback(*args, **kwargs)
        return True

    return GLib.timeout_add(parse_interval(time_ms), on_timeout)


def idle(callback: Callable, *args: Any, **kwargs: Any) -> int:
    """Schedule a callback function to be called whenever there
    are no higher priority events pending to the default PotatoLoop.
        Args:
            callback (Callable): The function to call when the main event loop is idle.

        Returns:
            int: The ID of the idle source.
    """

    def on_idle() -> bool:
        callback(*args, **kwargs)
        return False

    return GLib.idle_add(on_idle)


def lookup_icon(
    icon_name: str,
    size: Literal[8, 16, 32, 64, 128] = 128,
    path: bool = True,
    fallback: str = "application-x-addon-symbolic",
) -> Union[str, Gtk.IconInfo]:
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
    icon_info: Gtk.IconInfo
    theme: Gtk.IconTheme
    filename: str
    name: str

    if icon_name:
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

            if not icon_info:
                continue

            filename = icon_info.get_filename()

            if not filename:
                continue

            if path:
                return filename
            else:
                return icon_info
    return (
        lookup_icon(fallback, path=True) if path else lookup_icon(fallback, path=False)
    )


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
    line: str = ""
    file: str = ""
    _line: int = -1

    try:
        file, _line, _, line = traceback_extract_stack()[-2]
    except:
        pass

    try:
        _, stdout, stderr, state = GLib.spawn_command_line_sync(cmd)

        if line:
            print(
                f"getoutput Method is deprecated, use Bash.get_output() instead, called on line {_line}, in file {file}"
            )
        else:

            print(f"getoutput Method is deprecated, use Bash.get_output() instead")
        return stdout.decode() if state == 0 else stderr.decode()
    except:
        return ""


def make_async(func: Callable):
    """
    Decorator to execute a function in a separate thread without blocking the main thread.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function that runs asynchronously in a separate thread.

    Note:
        To update the interface, variables, or elements outside the thread, it's recommended
        to use `idle()` within the thread to ensure thread-safe operation.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> GLib.Thread:
        def run_in_thread(*args, **kwargs) -> None:
            func(*args, **kwargs)

        return GLib.Thread.new(func.__name__, run_in_thread, *args, **kwargs)

    return wrapper

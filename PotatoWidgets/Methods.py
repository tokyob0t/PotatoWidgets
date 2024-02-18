from .Imports import *


def parse_interval(interval: Union[int, str] = 1000) -> int:
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
        elif isinstance(interval, int):
            return int(interval)
    except (ValueError, IndexError):
        pass

    return int(interval)


def wait(time_ms: Union[str, int], callback: Callable) -> None:
    """Wait for a specified amount of time and then execute a callback function.

    Args:
        time_ms (Union[str, int]): The time to wait before executing the callback.
        callback (Callable): The function to call after the specified time has elapsed.
    """

    def on_timeout():
        callback()
        return False

    GLib.timeout_add(parse_interval(time_ms), on_timeout)


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

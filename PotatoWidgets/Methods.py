from .Imports import *
from .Variable import Poll


def wait(time_ms: Union[str, int], callback: Callable) -> None:
    def on_timeout():
        callback()
        return False

    GLib.timeout_add(Poll._parse_interval(time_ms), on_timeout)


def lookup_icon(
    icon_name: str,
    size: Literal[8, 16, 32, 64, 128] = 128,
    path: bool = True,
    fallback: str = "application-x-addon-symbolic",
) -> str:
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

    return "" if path else lookup_icon(fallback)

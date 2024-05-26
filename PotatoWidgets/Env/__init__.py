"""
This module includes various directories and files related to application caching, configuration,
notifications, and styling in the Potato application.

    DIR_HOME: Home directory path fetched from GLib environment.
    DIR_CONFIG: Configuration directory path within the home directory.
    DIR_CONFIG_POTATO: Directory path specific to Potato within the configuration directory.
    DIR_CURRENT: Current directory path using GLib or falling back to Potato's configuration directory.
    DIR_CACHE: Cache directory path based on XDG_CACHE_HOME or defaulting to the home directory's cache.
    DIR_CACHE_NOTIF: Directory for notifications within the cache directory.
    DIR_CACHE_NOTIF_IMAGES: Directory for notification images within the notification cache directory.
    FILE_CACHE_APPS: JSON file path for caching application data.
    FILE_CACHE_NOTIF: JSON file path for caching notification data.
    FILE_CACHE_CSS: Path to the CSS file used for styling within the cache directory.
"""

from ..Imports import *

__all__ = [
    "DIR_CACHE",
    "DIR_CONFIG",
    "DIR_CURRENT",
    "DIR_HOME",
    "DIR_CACHE_TRAY",
    "DIR_CONFIG_POTATO",
    "DIR_CACHE_NOTIF",
    "DIR_CACHE_NOTIF_IMAGES",
    "FILE_CACHE_APPS",
    "FILE_CACHE_CSS",
    "FILE_CACHE_NOTIF",
]

DIR_HOME: str = GLib.getenv("HOME")
DIR_CONFIG: str = DIR_HOME + "/.config"
DIR_CONFIG_POTATO: str = DIR_CONFIG + "/potato"
DIR_CURRENT: str = GLib.get_current_dir() or (DIR_CONFIG + "/potato")


DIR_CACHE: str = DIR_HOME + "/.cache/PotatoCache"
DIR_CACHE_TRAY: str = DIR_CACHE + "/Tray"
DIR_CACHE_NOTIF: str = f"{DIR_CACHE}/Notifications"
DIR_CACHE_NOTIF_IMAGES: str = f"{DIR_CACHE_NOTIF}/Img"


FILE_CACHE_APPS: str = f"{DIR_CACHE}/Applications.json"
FILE_CACHE_NOTIF: str = f"{DIR_CACHE_NOTIF}/Notifications.json"
FILE_CACHE_CSS: str = f"{DIR_CACHE}/Style.css"


for _dir in [
    DIR_HOME,
    DIR_CACHE,
    DIR_CONFIG,
    DIR_CACHE_NOTIF,
    DIR_CACHE_NOTIF_IMAGES,
    DIR_CACHE_TRAY,
]:
    if not GLib.file_test(_dir, GLib.FileTest.IS_DIR):
        GLib.mkdir_with_parents(_dir, 0o755)

for _file in [FILE_CACHE_APPS, FILE_CACHE_NOTIF]:
    if not GLib.file_test(_file, GLib.FileTest.EXISTS):
        GLib.file_set_contents(filename=_file, contents="")

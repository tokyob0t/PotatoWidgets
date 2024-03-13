from ..Imports import *

DIR_HOME: str = GLib.getenv("HOME")
DIR_CONFIG: str = DIR_HOME + "/.config"
DIR_CONFIG_POTATO: str = DIR_CONFIG + "/potato"
DIR_CURRENT: str = GLib.get_current_dir() or (DIR_CONFIG + "/potato")


DIR_CACHE: str = (
    GLib.getenv("XDG_CACHE_HOME") or (DIR_HOME + "/.cache")
) + "/PotatoCache"
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
]:
    if not GLib.file_test(_dir, GLib.FileTest.IS_DIR):
        GLib.mkdir_with_parents(_dir, 0o755)

for _file in [FILE_CACHE_APPS, FILE_CACHE_NOTIF]:
    if not GLib.file_test(_file, GLib.FileTest.EXISTS):
        GLib.file_set_contents(filename=_file, contents="")

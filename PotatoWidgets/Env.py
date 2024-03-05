from .Imports import *

DIR_HOME = GLib.getenv("HOME")
DIR_CONFIG = DIR_HOME + "/.config"

DIR_CACHE = (GLib.getenv("XDG_CACHE_HOME") or (DIR_HOME + "/.cache")) + "/PotatoCache"
DIR_CACHE_NOTIF = f"{DIR_CACHE}/Notifications"
DIR_CACHE_NOTIF_IMAGES = f"{DIR_CACHE_NOTIF}/Img"

FILE_CACHE_APPS = f"{DIR_CACHE}/Applications.json"
FILE_CACHE_NOTIF = f"{DIR_CACHE_NOTIF}/Notifications.json"

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

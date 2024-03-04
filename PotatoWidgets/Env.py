from .Imports import *

DIR_HOME = GLib.getenv("HOME")
DIR_CACHE = (GLib.getenv("XDG_CACHE_HOME") or (DIR_HOME + "/.cache")) + "/PotatoCache"
DIR_CONFIG = DIR_HOME + "/.config"

FILE_APPS_CACHE = f"{DIR_CACHE}/Applications.json"

for _dir in [DIR_HOME, DIR_CACHE, DIR_CONFIG]:
    if not GLib.file_test(_dir, GLib.FileTest.IS_DIR):
        GLib.mkdir_with_parents(_dir, 0o755)

for _file in [FILE_APPS_CACHE]:
    if not GLib.file_test(_file, GLib.FileTest.EXISTS):
        GLib.file_set_contents(filename=_file, contents="")

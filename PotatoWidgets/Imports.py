import argparse
import importlib
import json
import sys
import threading
from importlib.machinery import ModuleSpec
from importlib.util import module_from_spec, spec_from_file_location
from os.path import expanduser as os_expanduser
from os.path import expandvars as os_expandvars
from random import randint
from re import sub as re_sub
from traceback import extract_stack as traceback_extract_stack
from types import ModuleType
from typing import (Any, Callable, Dict, List, Literal, NoReturn, Optional,
                    Tuple, Union)

import dbus
import dbus.service
import gi
from dbus import SessionBus
from dbus.mainloop.glib import DBusGMainLoop

for n, v in {
    "Gdk": "3.0",
    "GdkPixbuf": "2.0",
    "Gio": "2.0",
    "GLib": "2.0",
    "GObject": "2.0",
    "Gtk": "3.0",
    "GtkLayerShell": "0.1",
    "Pango": "1.0",
}.items():
    try:
        gi.require_version(n, v)
    except Exception as r:
        print(r)

from gi.repository import (Gdk, GdkPixbuf, Gio, GLib, GObject, Gtk,
                           GtkLayerShell, Pango)

DBusGMainLoop(set_as_default=True)

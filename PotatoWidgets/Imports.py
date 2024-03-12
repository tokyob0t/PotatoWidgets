import argparse
import importlib
import inspect
import json
import subprocess
import sys
import threading
from random import randint
from re import sub as re_sub
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

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

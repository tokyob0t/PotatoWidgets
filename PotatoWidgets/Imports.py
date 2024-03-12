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
    "Adw": "1",
    "Gdk": "4.0",
    "GdkPixbuf": "2.0",
    "Gio": "2.0",
    "Glib": "2.0",
    "GObject": "2.0",
    "Gtk": "4.0",
    # "GtkLayerShell": "0.1",
    "Pango": "1.0",
}.items():
    try:
        gi.require_version(n, v)
    except Exception as r:
        print(r)


from gi.repository import Adw, Gdk, GdkPixbuf, Gio, GLib, GObject, Gtk, Pango

DBusGMainLoop(set_as_default=True)

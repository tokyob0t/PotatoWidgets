"""
Module that imports all the required libraries in a single file
"""

__all__ = [
    "argparse",
    "functools",
    "importlib",
    "io",
    "json",
    "sys",
    "threading",
    "dataclass",
    "ModuleSpec",
    "module_from_spec",
    "spec_from_file_location",
    "os_expanduser",
    "os_expandvars",
    "randint",
    "re_sub",
    "traceback_extract_stack",
    "ModuleType",
    "Any",
    "Callable",
    "Dict",
    "List",
    "Literal",
    "NoReturn",
    "Optional",
    "Tuple",
    "Type",
    "TypeVar",
    "Union",
    "dbus",
    "gi",
    "literal_eval",
    "SessionBus",
    "DBusGMainLoop",
    "G_MAXDOUBLE",
    "G_MAXINT",
    "G_MININT",
    "TYPE_STRING",
    "Gdk",
    "GdkPixbuf",
    "Gio",
    "GLib",
    "GObject",
    "Gtk",
    "GtkLayerShell",
    "Pango",
    "Playerctl",
]


import argparse
import functools
import importlib
import io
import json
import sys
import threading
from ast import literal_eval
from dataclasses import dataclass
from importlib.machinery import ModuleSpec
from importlib.util import module_from_spec, spec_from_file_location
from os.path import expanduser as os_expanduser
from os.path import expandvars as os_expandvars
from random import randint
from re import sub as re_sub
from traceback import extract_stack as traceback_extract_stack
from types import ModuleType
from typing import (Any, Callable, Dict, List, Literal, NoReturn, Optional,
                    Tuple, Type, TypeVar, Union)

import dbus
import dbus.service
import gi
from dbus import SessionBus
from dbus.mainloop.glib import DBusGMainLoop
from gi._propertyhelper import G_MAXDOUBLE, G_MAXINT, G_MININT, TYPE_STRING

for n, v in {
    "Gdk": "3.0",
    "GdkPixbuf": "2.0",
    "Gio": "2.0",
    "GLib": "2.0",
    "GObject": "2.0",
    "Gtk": "3.0",
    "GtkLayerShell": "0.1",
    "Pango": "1.0",
    "Playerctl": "2.0",
}.items():
    try:
        gi.require_version(n, v)
    except Exception as r:
        print(r)

from gi.repository import (Gdk, GdkPixbuf, Gio, GLib, GObject, Gtk,
                           GtkLayerShell, Pango, Playerctl)

DBusGMainLoop(set_as_default=True)

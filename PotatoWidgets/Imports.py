import argparse
import importlib
import inspect
import json
import subprocess
import sys
import threading
from random import randint
from typing import Any, Callable, List, Literal, Optional, Union

import dbus
import dbus.service
import gi
from dbus import SessionBus
from dbus.mainloop.glib import DBusGMainLoop

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GtkLayerShell", "0.1")
gi.require_version("GdkPixbuf", "2.0")
gi.require_version("GObject", "2.0")


from gi.repository import Gdk, GdkPixbuf, Gio, GLib, GObject, Gtk, GtkLayerShell, Pango

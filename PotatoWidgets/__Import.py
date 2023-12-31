import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GtkLayerShell", "0.1")

from gi.repository import (Gdk, GdkPixbuf, Gio, GLib, GObject, Gtk,
                           GtkLayerShell)

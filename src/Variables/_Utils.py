from ..__Import import *

def interval(interval, callback, bind=None):
    callback()
    id = GLib.timeout_add(GLib.PRIORITY_DEFAULT, interval, lambda: callback() or True)
    if bind:
        bind.connect('destroy', lambda _: GLib.source_remove(id))
    return id

def timeout(ms, callback):
    return GLib.timeout_add(GLib.PRIORITY_DEFAULT, ms, lambda: callback() or GLib.SOURCE_REMOVE)

def idle(callback, prio=GLib.PRIORITY_DEFAULT):
    return GLib.idle_add(prio, lambda: callback() or GLib.SOURCE_REMOVE)

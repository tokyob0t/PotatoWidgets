from .__Import import *


def wait(time_ms, callback):
    def on_timeout():
        callback()
        return False

    GLib.timeout_add(time_ms, on_timeout)

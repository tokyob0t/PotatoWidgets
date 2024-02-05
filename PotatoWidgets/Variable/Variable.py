from ..Imports import *


class Variable(GObject.Object):
    valuechanged = GObject.Signal()

    def __init__(self, initial_value):
        super().__init__()
        self._value = initial_value

    def get_value(self):
        return self._value

    def set_value(self, new_value):
        self._value = new_value
        self.emit("valuechanged")

    def bind(self, callback):
        self.connect(
            "valuechanged",
            # lambda out: GLib.idle_add(lambda: callback(out.get_value())),
            lambda out: callback(out.get_value()),
        )

    def __str__(self):
        return str(self._value)

from ..__Import import *


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

    def initial_value(self, value):
        self._value = value

    def connect(self, callback):
        def callback_wrapper():
            callback(self.get_value())
            return False

        super().connect("valuechanged", callback_wrapper)

        GObject.idle_add(callback_wrapper)

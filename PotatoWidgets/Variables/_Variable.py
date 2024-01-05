from ..__Import import *


class Variable(GObject.Object):
    valuechanged = GObject.Signal()

    def __init__(self, initial_value):
        super().__init__()
        self._value = initial_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.emit("valuechanged")

    def initial_value(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

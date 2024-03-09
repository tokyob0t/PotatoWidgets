from ..Env import *
from ..Imports import *
from ..Variable import Listener, Poll, Variable


class Service(GObject.Object):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    def bind(self, signal: str, initial_value: Any = 0):
        new_var = Variable(initial_value)

        self.connect(signal, lambda _, value: new_var.set_value(value))
        return new_var

    def emit(self, **kwargs):
        return super().emit(**kwargs)

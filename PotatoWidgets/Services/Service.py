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

        # Hacky Stuff Again
        _, _, _, text = traceback_extract_stack()[-2]
        index = text.find("=")

        if index != -1:
            setattr(new_var, "_name", text[:index].strip())
        else:
            setattr(new_var, "_name", "")

        self.connect(signal, lambda _, value: new_var.set_value(value))

        return new_var

    def emit(self, *args, **kwargs):
        return super().emit(*args, **kwargs)


class ServiceChildren(Service):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self) -> None:
        super().__init__()

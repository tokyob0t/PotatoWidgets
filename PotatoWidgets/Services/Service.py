from ..Env import *
from ..Imports import *
from ..Variable import Variable

__all__ = ["Service", "ServiceChildren"]


class Service(GObject.Object):

    _instance = None
    __gsignals__ = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    def bind(self, signal: str, initial_value: Any = 0):
        new_var = Variable(initial_value)

        _, _, _, line = traceback_extract_stack()[-2]
        index = line.find("=")

        if index != -1:
            setattr(new_var, "_name", line[:index].strip())
        else:
            setattr(new_var, "_name", "")

        self.connect(signal, lambda _, value: new_var.set_value(value))

        return new_var

    def emit(self, *args: Any, **kwargs: Any) -> Any:
        return super().emit(*args, **kwargs)

    """

    @staticmethod
    def register_prop():
        pass
    
    @staticmethod
    def gsignals(signals: Dict[str, List[str]]):
        SIGNAL_FLAGS = GObject.SignalFlags
        signals_dict = {}

        for signal, parameters in signals.items():
            new_parameters = [None, None, None]

            for i in parameters:
                signal_flags = {
                    "run-first": SIGNAL_FLAGS.RUN_FIRST,
                    "run-last": SIGNAL_FLAGS.RUN_LAST,
                    "run-cleanup": SIGNAL_FLAGS.RUN_CLEANUP,
                    "action": SIGNAL_FLAGS.ACTION,
                    "detailed": SIGNAL_FLAGS.DETAILED,
                    "no-hooks": SIGNAL_FLAGS.NO_HOOKS,
                    "no-recurse": SIGNAL_FLAGS.NO_RECURSE,
                    "deprecated": SIGNAL_FLAGS.DEPRECATED,
                    "must-collect": SIGNAL_FLAGS.MUST_COLLECT,
                    "accumulator": SIGNAL_FLAGS.ACCUMULATOR_FIRST_RUN,
                }.get(i, SIGNAL_FLAGS.RUN_LAST)

                if signal_flags:
                    new_parameters[0] = signal_flags

                if i == str:
                    new_parameters[2] = str
                elif i == int:
                    new_parameters[2]

                # "available": (GObject.SignalFlags.RUN_FIRST, None, (bool,)),
            signals_dict[signal] = tuple(parameters)


    """


class ServiceChildren(Service):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self) -> None:
        super().__init__()

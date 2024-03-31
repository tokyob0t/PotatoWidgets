from ..Env import *
from ..Imports import *
from ..Variable import Variable

__all__ = ["Service", "ServiceChildren"]


class Service(GObject.Object):

    _instance = None
    __gsignals__ = {}
    __gproperties__ = {}

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

    @staticmethod
    def properties(
        properties: Dict[str, List[Union[str, type]]],
        *,
        getter,
        setter,
        type,
        initial_value,
        name,
        description,
        flags,
        min,
        max,
    ):
        ParamFlags = GObject.ParamFlags
        _flags = {
            "deprecated": ParamFlags.DEPRECATED,
            "readable": ParamFlags.READABLE,
            "writable": ParamFlags.WRITABLE,
            "readwrite": ParamFlags.READWRITE,
            "explicit-notify": ParamFlags.EXPLICIT_NOTIFY,
            "static-blurb": ParamFlags.STATIC_BLURB,
            "static-name": ParamFlags.STATIC_NAME,
            "static-nick": ParamFlags.STATIC_NICK,
            "lax-validation": ParamFlags.LAX_VALIDATION,
            "private": ParamFlags.PRIVATE,
            "construct": ParamFlags.CONSTRUCT,
            "construct-only": ParamFlags.CONSTRUCT_ONLY,
            #
            "d": ParamFlags.DEPRECATED,
            "r": ParamFlags.READABLE,
            "w": ParamFlags.WRITABLE,
            "rw": ParamFlags.READWRITE,
            "en": ParamFlags.EXPLICIT_NOTIFY,
            "sb": ParamFlags.STATIC_BLURB,
            "sna": ParamFlags.STATIC_NAME,
            "sni": ParamFlags.STATIC_NICK,
            "lax": ParamFlags.LAX_VALIDATION,
            "priv": ParamFlags.PRIVATE,
            "c": ParamFlags.CONSTRUCT,
            "co": ParamFlags.CONSTRUCT_ONLY,
        }.get(flags, ParamFlags.READWRITE)

        return Property(
            getter=getter,
            setter=setter,
            type=type,
            default=initial_value,
            nick=name,
            blurb=description,
            flags=_flags,
            minimum=min,
            maximum=max,
        )

    @staticmethod
    def signals(
        signals: Dict[str, List[Union[str, type, list]]] = {},
        *,
        flag: Literal[
            "run-first",
            "run-last",
            "run-cleanup",
            "action",
            "detailed",
            "no-hooks",
            "no-recurse",
            "deprecated",
            "must-collect",
            "accumulator",
        ] = "run-first",
        signal_name: str = "",
    ) -> Dict[
        str,
        Tuple[
            GObject.SignalFlags,
            Union[type, None],
            Tuple[type, ...],
        ],
    ]:
        SignalFlags = GObject.SignalFlags
        new_gsignals = {}
        if signals:
            for signal, parameters in signals.items():

                new_parameters = [SignalFlags.RUN_FIRST, None, []]
                for i in parameters:
                    if isinstance(i, (type)):
                        new_parameters[1] = i
                    elif isinstance(i, (list)):
                        new_parameters[2] = i
                    elif isinstance(i, (str)):
                        new_parameters[0] = {
                            "run-first": SignalFlags.RUN_FIRST,
                            "run-last": SignalFlags.RUN_LAST,
                            "run-cleanup": SignalFlags.RUN_CLEANUP,
                            "action": SignalFlags.ACTION,
                            "detailed": SignalFlags.DETAILED,
                            "no-hooks": SignalFlags.NO_HOOKS,
                            "no-recurse": SignalFlags.NO_RECURSE,
                            "deprecated": SignalFlags.DEPRECATED,
                            "must-collect": SignalFlags.MUST_COLLECT,
                            "accumulator": SignalFlags.ACCUMULATOR_FIRST_RUN,
                        }.get(i, SignalFlags.RUN_FIRST)

                new_parameters[2] = tuple(new_parameters[2])
                new_gsignals[signal] = tuple(new_parameters)

            return new_gsignals
        else:
            return {}


class ServiceChildren(Service):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def __init__(self) -> None:
        super().__init__()

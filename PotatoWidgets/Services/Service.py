from ..Env import *
from ..Imports import *
from ..Variable import Variable

__all__ = ["Service", "ServiceChildren"]


class Service(GObject.Object):

    _instance = None
    __gsignals__: Dict[
        str,
        Tuple[
            GObject.SignalFlags,
            Union[type, None],
            Tuple[type, ...],
        ],
    ] = {}
    __gproperties__: Dict[str, tuple] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    def emit(self, *args: Any, **kwargs: Any) -> Any:
        return super().emit(*args, **kwargs)

    def notify(self, property_name: str = None) -> None:
        return super().notify(property_name)

    # def connect(self, signal_spec: str = None, *args: Any) -> object:
    #    try:
    #        return self.connect("notify::" + signal_spec, *args)
    #    except:
    #        pass
    #    try:
    #        return self.connect(signal_spec, *args)
    #    except Exception as r:
    #        raise r

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

    def get_property(self, property_name: str) -> Union[Any, None]:
        privprop_name: str = "_" + property_name.lower()

        if hasattr(self, privprop_name):
            return getattr(self, privprop_name)

    def set_property(self, property_name: str, value: Any = None) -> None:
        signal_name: str = property_name.lower().replace("_", "-")
        privprop_name: str = "_" + property_name.lower()

        if hasattr(self, privprop_name):
            setattr(self, privprop_name, value)
            self.notify(signal_name)

    @staticmethod
    def properties(
        properties: Dict[str, List[Union[str, type]]],
    ):
        if not properties:
            return {}

        ParamFlags = GObject.ParamFlags
        new_gprops: Dict[str, tuple] = {}
        #
        allowed_types: List[type] = [int, str, bool, float, object]

        _flags: Dict[str, GObject.ParamFlags] = {
            "readable": ParamFlags.READABLE,
            "writable": ParamFlags.WRITABLE,
            "readwrite": ParamFlags.READWRITE,
            "deprecated": ParamFlags.DEPRECATED,
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
            "lv": ParamFlags.LAX_VALIDATION,
            "priv": ParamFlags.PRIVATE,
            "c": ParamFlags.CONSTRUCT,
            "co": ParamFlags.CONSTRUCT_ONLY,
        }

        for prop_name, prop_props in properties.items():
            default_structure: List[
                Union[
                    type,
                    int,
                    bool,
                    str,
                    float,
                    GObject.ParamFlags,
                ]
            ] = [
                "type",
                prop_name,
                prop_name,
                # "nick-name",
                # "description",
            ]

            if not prop_props or not isinstance(prop_props[0], type):
                continue
            if prop_props[0] not in allowed_types:
                prop_props[0] = object

            if prop_props[0] in [str, bool]:
                default_structure += [
                    False if prop_props[0] == bool else "",
                ]
            elif prop_props[0] in [int, float]:
                default_structure += (
                    [
                        GLib.MININT,  # noqa
                        GLib.MAXINT,  # noqa
                        0,
                    ]  # MAXINT/MININT not member of module Glib bablabla
                    if prop_props[0] == int
                    else [
                        -GLib.MINFLOAT,  # noqa
                        GLib.MAXFLOAT,  # noqa
                        0.0,
                    ]  # MAXFLOAT/MINFLOAT not member of module Glib bablabla
                )

            default_structure += [ParamFlags.READABLE]

            for i in prop_props:
                if isinstance(i, (type)):
                    default_structure[0] = i
                elif isinstance(i, (str)):
                    if i.startswith("n:"):
                        default_structure[1] = i.lstrip("n:")
                    elif i.startswith("d:"):
                        default_structure[2] = i.lstrip("d:")
                    elif i in _flags:
                        default_structure[-1] = _flags.get(i, ParamFlags.READABLE)

                    else:
                        default_structure[1], default_structure[2] = prop_name

                new_gprops[prop_name] = tuple(default_structure)

        return new_gprops

    @staticmethod
    def signals(
        signals: Dict[str, List[Union[str, type, list]]] = {},
    ) -> Dict[
        str,
        Tuple[
            GObject.SignalFlags,
            Union[type, None],
            Tuple[type, ...],
        ],
    ]:
        if not signals:
            return {}

        SignalFlags = GObject.SignalFlags
        new_gsignals = {}

        if signals:
            for signal, parameters in signals.items():

                default_structure = [SignalFlags.RUN_FIRST, None, []]
                for i in parameters:
                    if isinstance(i, (type)):
                        default_structure[1] = i
                    elif isinstance(i, (list)):
                        default_structure[2] = i
                    elif isinstance(i, (str)):
                        default_structure[0] = {
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

                default_structure[2] = tuple(default_structure[2])
                new_gsignals[signal] = tuple(default_structure)

            return new_gsignals
        else:
            return {}

    @staticmethod
    def make_property(instance: object, prop_name: str) -> None:
        private_name: str = "_" + prop_name
        # val_type: type = type(getattr(instance, private_name, None))
        # if val_type is None:
        #    return

        # def getter(self) -> val_type:
        def getter(self):
            return getattr(self, private_name)

        # def setter(self, value: val_type):
        def setter(self, value):
            self.notify(prop_name)
            setattr(self, private_name, value)

        setattr(instance.__class__, prop_name, property(getter, setter))


class ServiceChildren(Service):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self) -> None:
        super().__init__()

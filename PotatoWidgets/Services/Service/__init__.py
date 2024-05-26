from ..._Logger import Logger
from ...Env import *
from ...Imports import *
from ...Methods import idle, parse_interval

__all__ = ["Service"]


class BaseGObjectClass(GObject.Object):

    __gproperties__: Dict[
        str,
        Union[
            Tuple[Type[object], str, str, GObject.ParamFlags],
            Tuple[Type[bool], str, str, bool, GObject.ParamFlags],
            Tuple[Type[str], str, str, str, GObject.ParamFlags],
            Tuple[Type[int], str, str, G_MININT, G_MAXINT, int, GObject.ParamFlags],
            Tuple[
                Type[float],
                str,
                str,
                G_MAXDOUBLE,
                G_MAXDOUBLE,
                float,
                GObject.ParamFlags,
            ],
        ],
    ]

    __gsignals__: Dict[
        str,
        Tuple[
            GObject.SignalFlags,
            Union[
                Type[str],
                Type[int],
                Type[bool],
                Type[float],
                Type[object],
                None,
            ],
            Tuple[
                Union[
                    Type[str],
                    Type[int],
                    Type[bool],
                    Type[float],
                    Type[object],
                    None,
                ],
                ...,
            ],
        ],
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def list_properties(self) -> Tuple[str, ...]:
        """
        List all properties of the service.

        Returns:
            tuple: A tuple containing all property names.
        """

        return tuple(i.name for i in super().list_properties())

    def list_signals(self) -> tuple:
        """
        List all signals emitted by the service.

        Returns:
            tuple: A tuple containing all signal names.
        """
        return tuple(GObject.signal_list_names(self))

    def emit(self, signal_name: str, *args: Any, **kwargs: Any) -> Union[Any, None]:
        """
        Emit a signal with specified arguments.

        Args:
            signal_name (str): The name of the signal to emit.
            *args (Any): Variable length argument list.
            **kwargs (Any): Arbitrary keyword arguments.

        Returns:
            Union[Any, None]: The return value of the signal emission.
        """
        if signal_name in self.list_properties():
            return super().notify(signal_name)
        elif signal_name in self.list_signals() or signal_name == "value-changed":
            return super().emit(signal_name, *args, **kwargs)
        else:
            Logger.DEBUG(
                f"signal/property {signal_name} not found in {self.__class__.__name__}"
            )

    def notify(self, property_name: str) -> None:
        """
        Notify observers about a property change.

        Args:
            property_name (str): The name of the property to notify about.

        Returns:
            None
        """
        return super().notify(property_name)

    def connect(
        self, signal_name: str, callback: Callable, *args: Any, **kwargs: Any
    ) -> Union[object, None]:
        """
        Connect a signal to a callback function.

        Args:
            signal_spec (str): The specification of the signal to connect.
            *args (Any): Variable length argument list for the callback.

        Returns:
            object: The connection object.
        """
        # return super().connect(signal_name, callback, *args, **kwargs)

        signal_name = (
            signal_name.replace("notify::", "")
            if signal_name.startswith("notify::")
            else signal_name
        )

        if signal_name == "value-changed":
            return super().connect(signal_name, callback, *args, **kwargs)

        if not self.__check_signal(signal_name):
            Logger.WARNING(
                f"signal {signal_name} not found in {self.__class__.__name__}"
            )

        if signal_name in self.list_properties():
            # return super().connect("notify::" + signal_name, callback)
            prop: str = "_" + signal_name.replace("-", "_")
            return super().connect(
                "notify::" + signal_name,
                lambda *args: callback(
                    (args[0] if len(args) > 1 else args),
                    self.property(prop),
                ),
                *args,
                **kwargs,
            )

        elif signal_name in self.list_signals():
            return super().connect(
                signal_name,
                callback,
                # lambda *args: (callback(*(args[1:])) if len(args) > 1 else callback()),
                *args,
                **kwargs,
            )
        else:
            return super().connect(signal_name, callback, *args, **kwargs)

    def bind(
        self, signal: str, format: Callable = lambda *value: value, *args, **kwargs
    ) -> "Variable":
        """
        Bind a variable to a signal/property emitted by the service.

        Args:
            signal (str): The name of the signal to bind to.
            format (Callable): The format function to apply to the value.

        Returns:
            Variable: The newly created bound variable.
        """

        if not isinstance(format, Callable):
            _, _, _, line = traceback_extract_stack()[-2]
            raise Exception(line)

        signal = (
            signal.replace("notify::", "") if signal.startswith("notify::") else signal
        )

        if not self.__check_signal(signal):
            raise Exception("Signal", signal, "doesnt exist")

        new_var = Variable("", format=format)

        _, _, _, line = traceback_extract_stack()[-2]
        index = line.find("=")

        if index != -1:
            setattr(new_var, "_name", line[:index].strip())
        else:
            setattr(new_var, "_name", "")

        if signal in self.list_properties():
            prop = "_" + signal.replace("-", "_")

            new_var.set_value(self.property(prop))

        self.connect(signal, lambda _, val: new_var.set_value(val, *args, **kwargs))

        return new_var

    def property(self, property: str, new_value: Any = None) -> Union[None, Any]:
        """
        Get or set the value of a property. Its like setattr/getattr but using notify
        to emit a signal if the value changes.

        Args:
            property_name (str): The name of the property.
            new_value (Any, optional): The new value for the property. Defaults to None.

        Returns:
            Union[None, Any]: The current value of the property or None if setting.
        """
        if hasattr(self, property):

            if new_value is not None:
                if property.startswith("__"):
                    signal = property[2:].replace("_", "-")
                elif property.startswith("_"):
                    signal = property[1:].replace("_", "-")
                else:
                    signal = property

                if signal not in self.list_properties():
                    Logger.WARNING(
                        f"signal property {signal} not found in {self.__class__.__name__}"
                    )
                    return
                else:
                    setattr(
                        self,
                        property,
                        new_value,
                    )

                    self.emit(signal)

            else:
                return getattr(self, property)
        else:
            Logger.WARNING(
                f"{self.__class__.__name__} doesnt have the the property {property}"
            )

    def __check_signal(self, signal_name: str):

        if signal_name.startswith("notify::"):
            signal_name = signal_name.split("notify::")[0]

        if signal_name in (list(self.list_signals()) + list(self.list_properties())):
            return True
        else:
            Logger.WARNING(
                f"signal {signal_name} not found in {self.__class__.__name__}"
            )
            return False


class Service(BaseGObjectClass):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    def properties(
        properties: Dict[
            str,
            List[
                Union[
                    Literal[
                        "readable",
                        "writable",
                        "readwrite",
                        "deprecated",
                        "explicit-notify",
                        "static-blurb",
                        "static-name",
                        "static-nick",
                        "lax-validation",
                        "private",
                        "construct",
                        "construct-only",
                        #
                        "d",
                        "r",
                        "w",
                        "rw",
                        "en",
                        "sb",
                        "sna",
                        "sni",
                        "lv",
                        "priv",
                        "c",
                        "co",
                    ],
                    Type[str],
                    Type[int],
                    Type[bool],
                    Type[float],
                    Type[object],
                    str,
                ]
            ],
        ],
    ) -> Dict[
        str,
        Union[
            Tuple[Type[object], str, str, GObject.ParamFlags],
            Tuple[Type[bool], str, str, bool, GObject.ParamFlags],
            Tuple[Type[str], str, str, str, GObject.ParamFlags],
            Tuple[Type[int], str, str, G_MININT, G_MAXINT, int, GObject.ParamFlags],
            Tuple[
                Type[float],
                str,
                str,
                G_MAXDOUBLE,
                G_MAXDOUBLE,
                float,
                GObject.ParamFlags,
            ],
        ],
    ]:
        """
        Generate GObject properties from a dictionary.

        Args:
            properties (Dict[str, List[Union[str, type]]]): A dictionary containing property information.

        Returns:
            Dict[str, tuple]: A dictionary of GObject properties.

        Example:
        .. code-block:: python
            :linenos:
            :caption: Example of generating GObject properties.

            Service.signals(
                {
                    "notifications": [object],  # Since it's an array.
                    "popups": [object],  # Also this.
                    "count": [int],  # This data is an int.
                    "dnd": [bool],  # Boolean.
                }
            )
        """

        if not properties:
            return {}

        ParamFlags = GObject.ParamFlags
        new_gprops: Dict[str, tuple] = {}

        #
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
            prop_type: Union[type, None] = next(
                (i for i in prop_props if isinstance(i, type)), None
            )

            if not prop_props or prop_type is None:
                continue

            if prop_type in [str, bool]:
                default_structure += [
                    False if prop_type == bool else "",
                ]
            elif prop_type in [int, float]:
                default_structure += (
                    [
                        G_MININT,  # noqa
                        G_MAXINT,  # noqa
                        0,
                    ]
                    if prop_type == int
                    else [
                        -G_MAXDOUBLE,
                        G_MAXDOUBLE,
                        0.0,
                    ]
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
                        default_structure[1] = default_structure[2] = prop_name

                new_gprops[prop_name] = tuple(default_structure)

        return new_gprops

    @staticmethod
    def signals(
        signals: Dict[
            str,
            List[
                Union[
                    str,
                    Type[Union[str, int, bool, float, object, None]],
                    List[
                        Union[
                            Type[str],
                            Type[int],
                            Type[bool],
                            Type[float],
                            Type[object],
                            None,
                        ]
                    ],
                ]
            ],
        ] = {},
    ) -> Dict[
        str,
        Tuple[
            GObject.SignalFlags,
            Union[Type[str], Type[int], Type[bool], Type[float], Type[object], None],
            Tuple[
                Union[
                    Type[str], Type[int], Type[bool], Type[float], Type[object], None
                ],
                ...,
            ],
        ],
    ]:
        """
        Generate GObject signals from a dictionary.

        Args:
            signals (Dict[str, List[Union[str, type, list]]], optional): A dictionary containing signal information. Defaults to {}.

        Returns:
            Dict[str, Tuple[GObject.SignalFlags, Union[type, None], Tuple[type, ...]]]: A dictionary of GObject signals.
        """
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

    # @staticmethod
    # def make_property(instance: object, prop_name: str) -> None:
    #    """
    #    Create a GObject property for a given instance.
    #
    #     Args:
    #         instance (object): The instance for which to create the property.
    #         prop_name (str): The name of the property.
    #     Returns:
    #         None
    #    """
    #    private_name: str = "_" + prop_name
    #
    #    def getter(self):
    #        return getattr(self, private_name)
    #
    #    def setter(self, value):
    #        self.notify(prop_name)
    #        setattr(self, private_name, value)
    #        setattr(instance.__class__, prop_name, property(getter, setter))


class Variable(BaseGObjectClass):
    """
    Represents a variable with the ability to bind to a callback function.

    Signals:
        valuechanged: A signal emitted when the value of the variable changes.

    Attributes:
        value: The current value of the variable.
    """

    __gsignals__ = Service.signals({"value-changed": []})
    __gproperties__ = Service.properties({"value": [object]})

    def __init__(
        self, initial_value: Any = "", *, format: Callable = lambda value: value
    ) -> None:
        """
        Initializes a Variable object.

        Args:
            initial_value (Any): The initial value for the variable. Defaults to an empty string.
        """
        super().__init__()
        self._value: Any = None
        self._format: Callable = format
        self.value = initial_value

        # Hacky Stuff
        line: str
        index: int
        _, _, _, line = traceback_extract_stack()[-2]
        index = line.find("=")

        if index != -1:
            self._name: str = line[:index].strip()
        else:
            self._name: str = ""

    @property
    def format(self) -> Callable:
        return self._format

    @format.setter
    def format(self, callback: Callable) -> None:
        self._format = callback

    def get_value(self) -> Any:
        """
        Get the current value of the variable.

        Returns:
            Any: The current value of the variable.
        """
        return self.value

    def set_value(self, new_value: Any) -> None:
        """
        Set a new value for the variable and emit the 'valuechanged' signal.

        Args:
            new_value: The new value for the variable.
        """
        self.value = new_value

    @property
    def value(self) -> Any:
        """
        Get the current value of the variable using a property.

        Returns:
            Any: The current value of the variable.
        """
        return self._value

    @value.setter
    def value(self, new_value: Any = None) -> None:
        """
        Set a new value for the variable using a property and emit the 'value-changed' signal.

        Args:
            new_value: The new value for the variable.
        """
        self._value = new_value
        self.emit("value-changed")
        self.emit("value")

    def bind(
        self,
        callback: Callable,
        format: Union[Callable, None] = None,
        *args,
        **kwargs,
    ) -> object:
        """
        Bind a callback function to the 'value-changed' signal.

        Args:
            callback: The callback function to bind.
        """
        if format:
            self.format = format

        return self.connect(
            "value-changed",
            lambda _self_: idle(callback, self.format(_self_.value), *args, **kwargs),
            # lambda _self_: callback(_self_.value, *args, **kwargs),
        )

    @property
    def __name__(self) -> str:
        return self._name

    def __str__(self) -> str:
        return str(self.value)
        # return f"{self.__name__}(value={self._value})"

    def __repr__(self) -> str:
        return self.__str__()


class Poll(Variable):
    """
    Represents a variable that polls a callback function at regular intervals.

    Attributes:
        _interval: The polling interval in milliseconds.
        _callback: The callback function to poll.
        _timeout_id: Identifier for the timeout source used for polling.
    """

    def __init__(
        self, interval: Union[int, str], callback: Callable, initial_value: Any = ""
    ) -> None:
        """
        Initializes a Poll object.

        Args:
            interval (Union[int, str]): The polling interval in milliseconds, or a string representing a time interval.
            callback (Callable): The callback function to poll.
            initial_value (Any): The initial value for the poll. Defaults to an empty string.
        """
        super().__init__(initial_value or callback())
        self._interval = parse_interval(interval)
        self._callback = callback
        self._timeout_id = None
        self.start_poll()

    def is_polling(self) -> bool:
        """
        Check if the poll is currently active.

        Returns:
            bool: True if the poll is active, False otherwise.
        """
        return bool(self._timeout_id)

    def stop_poll(self) -> None:
        """
        Stop the polling process.
        """
        if self._timeout_id:
            GLib.source_remove(self._timeout_id)
            self._timeout_id = None
        else:
            print(f"{self} has no poll running")

    def start_poll(self) -> None:
        """
        Start the polling process.
        """
        if self.is_polling():
            print(f"{self} is already polling")
            return

        self._timeout_id = GLib.timeout_add(
            interval=self._interval or 1000,
            function=self._poll_callback,
        )

    def _poll_callback(self):
        """
        Internal method to execute the callback function and update the value.
        """
        self.value = self._callback()
        return True


class Listener(Variable):
    """
    Represents a variable that listens for updates from a callback function running in a separate thread.
    """

    def __init__(self, callback: Callable, initial_value: Any = "") -> None:
        """
        Initializes a Listener object.

        Args:
            callback (Callable): The callback function to listen to for updates.
            initial_value (Any): The initial value for the listener. Defaults to an empty string.
        """
        super().__init__(initial_value)
        self._callback = callback
        self._thread = GLib.Thread.new(
            f"{initial_value=}-{self._callback.__name__}", self._exec_callback
        )

    def _exec_callback(self) -> None:
        """
        Internal method to execute the callback function in a separate thread.
        """
        for line in self._callback():
            self.set_value(line)

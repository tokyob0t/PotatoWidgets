from ..Imports import *
from .Service import Service


class BatteryService(Service):
    # __gsignals__ = {
    #    "available": (GObject.SignalFlags.RUN_FIRST, None, (bool,)),
    #    "percentage": (GObject.SignalFlags.RUN_FIRST, None, (int,)),
    #    "state": (GObject.SignalFlags.RUN_FIRST, None, (int,)),
    #    "icon-name": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    #    "time-remaining": (GObject.SignalFlags.RUN_FIRST, None, (int,)),
    #    "energy": (GObject.SignalFlags.RUN_FIRST, None, (float,)),
    #    "energy-full": (GObject.SignalFlags.RUN_FIRST, None, (float,)),
    #    "energy-rate": (GObject.SignalFlags.RUN_FIRST, None, (float,)),
    # }
    __gsignals__ = Service.signals(
        {
            "available": [[bool]],
            "percentage": [[int]],
            "state": [[int]],
            "icon-name": [[str]],
            "time-remaining": [[int]],
            "energy": [[float]],
            "energy-full": [[float]],
            "energy-rate": [[float]],
        }
    )
    __gproperties__ = Service.properties({""})

    def __init__(self, battery: str = "/org/freedesktop/UPower/devices/battery_BAT1"):
        super().__init__()

        self._battery = battery

        self._available: bool = False
        self._percentage: int = -1
        self._state: int = 0
        self._icon_name: str = "battery-missing-symbolic"
        self._time_remaining: int = 0

        self._UPOWER_NAME = "org.freedesktop.UPower"
        self._UPOWER_PATH = "/org/freedesktop/UPower"

        self._DBUS_PROPERTIES = "org.freedesktop.DBus.Properties"
        self._bus = dbus.SystemBus()

        self._proxy = self._bus.get_object(self._UPOWER_NAME, self._battery)
        self._interface = dbus.Interface(self._proxy, self._DBUS_PROPERTIES)
        self._interface.connect_to_signal("PropertiesChanged", self._get_all)

    def bind(
        self,
        signal: Literal[
            "available",
            "percentage",
            "state",
            "icon-name",
            "time-remaining",
            "energy",
            "energy-full",
            "energy-rate",
        ],
        initial_value: Any = 0,
    ):
        return super().bind(signal, initial_value)

    def _get_all(self, *_) -> None:

        if not self._interface_prop("IsPresent"):
            self._available = False
            return

        data_key_value = {
            "_available": "IsPresent",
            "_percentage": "Percentage",
            "_state": "State",
            "_icon_name": "IconName",
            "_time_remaining": "TimeTo",
        }

        for key, value in data_key_value.items():
            value = self._interface_prop(value)

            if value != getattr(self, key):
                setattr(self, key, value)

                _signal = key[1:].lower().replace("_", "-")  # kebab-case for signals

                self.emit(_signal, value)

            else:
                continue

    def _interface_prop(self, prop: str) -> Any:
        if prop == "TimeTo":
            if self._interface_prop("State") == 1:
                _val = self._interface_prop("TimeToFull")
            else:
                _val = self._interface_prop("TimeToEmpty")
        else:
            _val = self._interface.Get(self._UPOWER_NAME + ".Device", prop)

        return _val

    @property
    def available(self) -> bool:
        return self._available

    @property
    def percentage(self) -> int:
        return self._percentage

    @property
    def icon_name(self) -> str:
        return self._icon_name

    @property
    def time_remaining(self) -> int:
        return self._time_remaining

    @property
    def state(self) -> int:
        return self._state

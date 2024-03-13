from .Imports import *
from .Methods import parse_interval


class Variable(GObject.Object):
    """
    Represents a variable with the ability to bind to a callback function.

    Signals:
        valuechanged: A signal emitted when the value of the variable changes.

    Attributes:
        _value: The current value of the variable.
    """

    valuechanged = GObject.Signal()

    def __init__(self, initial_value: Any = "") -> None:
        """
        Initializes a Variable object.

        Args:
            initial_value (Any): The initial value for the variable. Defaults to an empty string.
        """
        super().__init__()
        self._value: Any = initial_value

        # Hacky Stuff
        _, _, _, text = traceback_extract_stack()[-2]
        index: int = text.find("=")

        if index != -1:
            self._name: str = text[:index].strip()
        else:
            self._name: str = ""

    def get_value(self) -> Any:
        """
        Get the current value of the variable.

        Returns:
            Any: The current value of the variable.
        """
        return self._value

    def set_value(self, new_value: Any) -> None:
        """
        Set a new value for the variable and emit the 'valuechanged' signal.

        Args:
            new_value: The new value for the variable.
        """
        self._value = new_value
        self.emit("valuechanged")

    @property
    def value(self) -> Any:
        """
        Get the current value of the variable using a property.

        Returns:
            Any: The current value of the variable.
        """
        return self._value

    @value.setter
    def value(self, new_value: Any) -> None:
        """
        Set a new value for the variable using a property and emit the 'valuechanged' signal.

        Args:
            new_value: The new value for the variable.
        """
        self._value = new_value
        self.emit("valuechanged")

    def bind(self, callback: Callable) -> None:
        """
        Bind a callback function to the 'valuechanged' signal.

        Args:
            callback: The callback function to bind.
        """
        self.connect(
            "valuechanged",
            lambda out: GLib.idle_add(lambda: callback(out.get_value())),
        )

    def emit(self, *args, **kwargs) -> None:
        super().emit(*args, **kwargs)

    @property
    def __name__(self) -> str:
        return self._name

    def __str__(self) -> str:
        """
        Return a string representation of the variable.

        Returns:
            str: A string representation of the variable.
        """
        return str(self._value)

    def __repr__(self) -> str:
        return str(self._value)


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
        self.set_value(self._callback())
        return GLib.SOURCE_CONTINUE


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
        self._thread = None
        self._stop_thread = threading.Event()
        self.start_listening()

    def stop_listening(self) -> None:
        """
        Stop the listening thread.
        """
        if self._thread and self._thread.is_alive():
            self._stop_thread.set()
            self._thread.join()

    def start_listening(self) -> None:
        """
        Start the listening thread.
        """
        if self._thread and self._thread.is_alive():
            print(f"{self} is already listening")
            return

        self._stop_thread.clear()
        self._thread = threading.Thread(target=self._exec_callback)
        self._thread.start()

    def _exec_callback(self) -> None:
        """
        Internal method to execute the callback function in a separate thread.
        """
        for line in self._callback():
            self.set_value(line)

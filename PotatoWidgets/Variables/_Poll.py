from ..__Import import *
from ._Variable import Variable


class Poll(Variable):
    def __init__(self, interval, callback, initial_value=None):
        super().__init__(initial_value or callback())
        self._interval = interval
        self._callback = callback
        self._timeout_id = None
        self.start_poll()

    def is_polling(self):
        return bool(self._timeout_id)

    def stop_poll(self):
        if self._timeout_id:
            GLib.source_remove(self._timeout_id)
            self._timeout_id = None
        else:
            print(f"{self} has no poll running")

    def start_poll(self):
        if self.is_polling():
            print(f"{self} is already polling")
            return

        self._timeout_id = GLib.timeout_add(
            priority=GLib.PRIORITY_DEFAULT_IDLE,
            interval=self._interval,
            function=self._poll_callback,
        )

    def _poll_callback(self):
        self.set_value(self._callback())
        return GLib.SOURCE_CONTINUE

    def __str__(self):
        return str(self._value)

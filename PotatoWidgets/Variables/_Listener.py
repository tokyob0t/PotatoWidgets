from ..__Import import *
from ._Variable import Variable


class Listener(Variable):
    def __init__(self, callback, initial_value=None):
        super().__init__(initial_value)
        self._callback = callback
        self._source_id = None
        self._first_run = True
        self.start_listening()

    def is_listening(self):
        return bool(self._source_id)

    def stop_listening(self):
        super().stop_listening()

    def start_listening(self):
        if self.is_listening():
            print(f"{self} is already listening")
            return
        self._source_id = GLib.idle_add(self._listen_callback)

    def _listen_callback(self):
        if self._first_run:
            self._callback(self.set_value)
            self._first_run = False
        return GLib.SOURCE_REMOVE

    def __str__(self):
        return str(self._value)

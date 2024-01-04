from ..__Import import *
from ._Variable import Variable


class Listener(Variable):
    def __init__(self, callback, initial_value=None):
        super().__init__(initial_value)
        self._callback = callback
        self._thread = None
        self._stop_thread = threading.Event()
        self.start_listening()

    def stop_listening(self):
        if self._thread and self._thread.is_alive():
            self._stop_thread.set()
            self._thread.join()

    def start_listening(self):
        if self._thread and self._thread.is_alive():
            print(f"{self} is already listening")
            return

        self._stop_thread.clear()
        self._thread = threading.Thread(target=lambda: self._callback(self))
        self._thread.start()

    def __str__(self):
        return str(self._value)

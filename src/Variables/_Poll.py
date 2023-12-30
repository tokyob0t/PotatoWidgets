from ..__Import import *


class Poll(GObject.GObject):
    value_changed = GObject.Signal()

    def __init__(self, interval, callback):
        super().__init__()
        self.interval = interval
        self.callback = callback
        self.timer_id = 0
        self._value = None
        self.start()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.value_changed.emit()

    def start(self):
        self.update()
        self.timer_id = GLib.timeout_add(self.interval, self.update)

    def stop(self):
        if self.timer_id:
            GLib.source_remove(self.timer_id)

    def update(self):
        self.value = self.callback()
        return True

    def __str__(self):
        return str(self.value) if self.value is not None else ""

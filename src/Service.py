from .__Import import GObject
from GObject import pspec, register_gobject, PspecFlag, PspecType
import json


def only_string(s):
    return s if isinstance(s, str) else None

class Binding:
    def __init__(self, emitter, prop):
        self.emitter = emitter
        self.prop = prop
        self.transform_fn = lambda v: v

    def transform(self, fn):
        bind = Binding(self.emitter, self.prop)
        prev = bind.transform_fn
        bind.transform_fn = lambda v: fn(prev(v))
        return bind

class Service(GObject.Object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def pspec(name, type='jsobject', handle='r'):
        return pspec(name, type, handle)

    @staticmethod
    def register(service, signals=None, properties=None):
        register_gobject(service, signals, properties)

    def connect(self, signal='changed', callback=None):
        return super().connect(signal, callback)

    def update_property(self, prop, value):
        if getattr(self, prop, None) == value or json.dumps(getattr(self, prop, None)) == json.dumps(value):
            return

        private_prop = ''.join(w.capitalize() if i > 0 else w for i, w in enumerate(prop.split('-')))
        setattr(self, f'_{private_prop}', value)
        self.notify(prop)

    def changed(self, property):
        self.notify(property)
        self.emit('changed')

    def bind(self, prop):
        return Binding(self, prop)

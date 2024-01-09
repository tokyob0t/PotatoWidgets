from ..__Import import *
from ._Common._BasicProps import BasicProps
from ._Common._Events import Events

class ToggleButton(Gtk.ToggleButton, BasicProps):
    def __init__(self,
        children = None,
        onclick = None,
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        active=True,
        visible=True,
        classname=""):
        
        Gtk.ToggleButton.__init__(self)

        BasicProps.__init__(self,
            halign = halign,
            valign = valign,
            hexpand = hexpand,
            vexpand = vexpand,
            active = active,
            visible = visible,
            classname = classname)
        
        self.add(children) if children else None

from ..__Import import *
from ._Common._BasicProps import BasicProps

class ComboBox(Gtk.ComboBoxText, BasicProps):
    def __init__(self,
        children = [],
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        active=True,
        visible=True,
        classname=""):


        Gtk.ComboBoxText.__init__(self)

        BasicProps.__init__(self,
            halign = halign,
            valign = valign,
            hexpand = hexpand,
            vexpand = vexpand,
            active = active,
            visible = visible,
            classname = classname)

        [self.add(i) for i in children if isinstance(i, Gtk.Widget)] 
        [self.append_text(i) for i in children if isinstance(i, str)] 
        
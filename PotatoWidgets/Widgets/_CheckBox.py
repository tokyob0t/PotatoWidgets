from ..__Import import *
from ._Button import Button

class CheckBox(Gtk.CheckButton, Button):
    def __init__(
        self,
        label="CheckButton",
        children=None,
        onclick=None,
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        active=True,
        visible=True,
        classname="",
    ):
        super().__init__()

        # Llama al constructor de Button
        Button.__init__(self,
            children = children,
            onclick = onclick,
            halign = halign,
            valign = valign,
            hexpand = hexpand,
            vexpand = vexpand,
            active = active,
            visible = visible,
            classname = classname
        )

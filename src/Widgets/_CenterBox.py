from ..__Import import *
from ._Common._BasicProps import BasicProps

class CenterBox(Gtk.Box, BasicProps):
    def __init__(self, orientation="h", start=Gtk.Box(), center=Gtk.Box(), end=Gtk.Box(), classname=""):

        Gtk.Box.__init__(self)
        BasicProps.__init__(self,
            halign="fill",
            valign="fill",
            hexpand=False,
            vexpand=False,
            active=None,
            visible=True,
            classname=classname)

        self.set_orientation(self.__clasif_orientation(orientation))
        self.pack_start(start, True, True, 0)
        self.pack_end(end, True, True, 0)
        self.set_center_widget(center)
        
    def __clasif_orientation(self, orientation):
        if orientation.lower() in ["vertical", "v", 0, False]:
            return Gtk.Orientation.VERTICAL
        elif orientation.lower() in ["horizontal", "h", 1, True]:
            return Gtk.Orientation.HORIZONTAL

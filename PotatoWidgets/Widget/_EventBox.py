from ..__Import import *
from ._Common._BasicProps import BasicProps
from ._Common._Events import Events


class EventBox(Gtk.EventBox, Events, BasicProps):
    def __init__(
        self,
        children=None,
        onclick=None,
        onmiddleclick=None,
        onhover=None,
        onhoverlost=None,
        onscrollup=None,
        onscrolldown=None,
        primaryhold=None,
        primaryrelease=None,
        secondaryhold=None,
        secondaryrelease=None,
        attributes=None,
        css=None,
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        visible=True,
        classname="",
    ):
        Gtk.EventBox.__init__(self)

        BasicProps.__init__(
            self,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=None,
            visible=visible,
            classname=classname,
        )

        self.add(children) if children else None
        attributes(self) if attributes else None

        self._scrollup = onscrollup
        self._scrolldown = onscrolldown

        self.connect("button-press-event", onclick)
        self.connect("button-release-event", onmiddleclick)
        self.connect("enter-notify-event", onhover)
        self.connect("leave-notify-event", onhoverlost)
        self.connect("scroll-event", self.__clasif_scroll)
        self.connect("key-press-event", primaryhold)
        self.connect("key-release-event", primaryrelease)
        self.connect("key-press-event", secondaryhold)
        self.connect("key-release-event", secondaryrelease)

    def __clasif_scroll(self, _, param):
        if param == Gdk.ScrollDirection.UP:
            if self._scrollup:
                self._scrollup()
        elif param == Gdk.ScrollDirection.DOWN:
            if self._scrolldown:
                self._scrolldown()
        print(param)

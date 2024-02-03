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
        self.dict = {
            "onclick": onclick,
            "onmiddleclick": onmiddleclick,
            "onhover": onhover,
            "onhoverlost": onhoverlost,
            "primaryhold": primaryhold,
            "primaryrelease": primaryrelease,
            "secondaryhold": secondaryhold,
            "secondaryrelease": secondaryrelease,
            "onscrollup": onscrollup,
            "onscrolldown": onscrolldown,
        }

        self.connect("scroll-event", self.__clasif_scroll)
        self.connect("button-press-event", self.__press_event)
        self.connect("button-release-event", self.__release_event)
        self.connect("enter-notify-event", self.__enter_event)
        self.connect("leave-notify-event", self.__leave_event)
        # self.connect("key-press-event", self.__press_event)
        # self.connect("key-release-event", self.__release_event)

    def __click_event(self, _):
        callback = self.dict.get("onclick", None)
        if callback:
            callback()

    def __clasif_scroll(self, _, param):
        if param == Gdk.ScrollDirection.UP:
            callback = self.dict.get("onscrollup", None)
            if callback:
                callback()
        elif param == Gdk.ScrollDirection.DOWN:
            callback = self.dict.get("onscrolldown", None)
            if callback:
                callback()

    def __press_event(self, _, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            callback = self.dict.get("primaryhold", None)
            if callback:
                callback()
                return
        elif event.button == Gdk.BUTTON_SECONDARY:
            callback = self.dict.get("secondaryhold", None)
            if callback:
                callback()
        elif event.button == Gdk.BUTTON_MIDDLE:
            callback = self.dict.get("onmiddleclick", None)
            if callback:
                callback()

    def __release_event(self, _, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            callback = self.dict.get("primaryrelease", None)
            if callback:
                callback()
        elif event.button == Gdk.BUTTON_SECONDARY:
            callback = self.dict.get("secondaryrelease", None)
            if callback:
                callback()

    def __enter_event(self, *_):
        callback = self.dict.get("onhover", None)
        if callback:
            callback()

    def __leave_event(self, *_):
        callback = self.dict.get("onhoverlost", None)
        if callback:
            callback()

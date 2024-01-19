from ..__Import import *
from ._Common._BasicProps import BasicProps


class Button(Gtk.Button, BasicProps):
    def __init__(
        self,
        children=None,
        onclick=None,
        onmiddleclick=None,
        onhover=None,
        onhoverlost=None,
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
        active=True,
        visible=True,
        classname="",
    ):
        Gtk.Button.__init__(self)
        BasicProps.__init__(
            self,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=active,
            visible=visible,
            classname=classname,
        )

        attributes(self) if attributes else None

        if children:
            self.add(children)

        self.dict = {
            "onclick": onclick,
            "onmiddleclick": onmiddleclick,
            "onhover": onhover,
            "onhoverlost": onhoverlost,
            "primaryhold": primaryhold,
            "primaryrelease": primaryrelease,
            "secondaryhold": secondaryhold,
            "secondaryrelease": secondaryrelease,
        }

        self.connect("clicked", self.__click_event_idle) if onclick else None
        self.connect("button-press-event", self.__press_event)
        self.connect("button-release-event", self.__release_event)
        self.connect("enter-notify-event", self.__enter_event)
        self.connect("leave-notify-event", self.__leave_event)

    def __click_event_idle(self, _):
        GLib.idle_add(self.__click_event)

    def __press_event(self, _, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            GLib.idle_add(self.__primaryhold_event)
        elif event.button == Gdk.BUTTON_SECONDARY:
            GLib.idle_add(self.__secondaryhold_event)
        elif event.button == Gdk.BUTTON_MIDDLE:
            GLib.idle_add(self.__onmiddleclick_event)

    def __release_event(self, _, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            GLib.idle_add(self.__primaryrelease_event)
        elif event.button == Gdk.BUTTON_SECONDARY:
            GLib.idle_add(self.__secondaryrelease_event)

    def __enter_event(self, *_):
        GLib.idle_add(self.__hover_event)

    def __leave_event(self, *_):
        GLib.idle_add(self.__hoverlost_event)

    def __click_event(self):
        callback = self.dict.get("onclick", None)
        if callback:
            callback()

    def __primaryhold_event(self):
        callback = self.dict.get("primaryhold", None)
        if callback:
            callback()

    def __primaryrelease_event(self):
        callback = self.dict.get("primaryrelease", None)
        if callback:
            callback()

    def __secondaryhold_event(self):
        callback = self.dict.get("secondaryhold", None)
        if callback:
            callback()

    def __secondaryrelease_event(self):
        callback = self.dict.get("secondaryrelease", None)
        if callback:
            callback()

    def __onmiddleclick_event(self):
        callback = self.dict.get("onmiddleclick", None)
        if callback:
            callback()

    def __hover_event(self):
        callback = self.dict.get("onhover", None)
        if callback:
            callback()

    def __hoverlost_event(self):
        callback = self.dict.get("onhoverlost", None)
        if callback:
            callback()

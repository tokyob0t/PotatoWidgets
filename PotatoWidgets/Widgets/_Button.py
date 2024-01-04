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
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=active,
            visible=visible,
            classname=classname,
        )

        self.set_property(
            "halign", Gtk.Align.FILL if halign == "fill" else Gtk.Align.START
        )
        self.set_property(
            "valign", Gtk.Align.FILL if valign == "fill" else Gtk.Align.START
        )
        self.set_property("hexpand", hexpand)
        self.set_property("vexpand", vexpand)
        self.set_property("sensitive", active)
        self.set_property("visible", visible)
        self.get_style_context().add_class(classname)

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

        self.connect("button-press-event", self.__press_event)
        self.connect("button-release-event", self.__release_event)
        self.connect("enter-notify-event", self.__enter_event)
        self.connect("leave-notify-event", self.__leave_event)

        # Llamar a __click_event a través de glib_idle_add para el evento "clicked"
        self.connect("clicked", self.__click_event_idle) if onclick else None

    def __click_event_idle(self, _):
        # Ejecutar __click_event en el bucle de eventos principal usando glib_idle_add
        GLib.idle_add(self.__click_event)

    def __click_event(self):
        callback = self.dict.get("onclick", None)
        if callback:
            callback()

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

    def __enter_event(self, *_):
        GLib.idle_add(self.__hover_event)

    def __leave_event(self, *_):
        GLib.idle_add(self.__hoverlost_event)

    def __hover_event(self):
        callback = self.dict.get("onhover", None)
        if callback:
            callback()

    def __hoverlost_event(self):
        callback = self.dict.get("onhoverlost", None)
        if callback:
            callback()

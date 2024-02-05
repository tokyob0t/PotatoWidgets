from ..Imports import *
from .Common import BasicProps
from ..Variable import Listener, Poll, Variable


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

    # Classification
    def __clasif_args(self, widget, event, callback):
        arg_num = callback.__code__.co_argcount
        arg_tuple = callback.__code__.co_varnames[:arg_num]

        if arg_num == 2:
            # GLib.idle_add(lambda: callback(widget=widget, event=event))
            callback(widget=widget, event=event)

        elif arg_num == 1:
            if "widget" in arg_tuple and widget:
                # GLib.idle_add(lambda: callback(widget=widget))
                callback(widget=widget)
            elif "event" in arg_tuple and event:
                # GLib.idle_add(lambda: callback(event=event))
                callback(event=event)
            else:
                # GLib.idle_add(lambda: callback(event))
                callback(event)
        else:
            # GLib.idle_add(callback)
            callback()

    def __click_event_idle(self, event):
        callback = self.dict.get("onclick")

        if callback:
            self.__clasif_args(widget=False, event=event, callback=callback)

    def __press_event(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            callback = self.dict.get("primaryhold")
        elif event.button == Gdk.BUTTON_SECONDARY:
            callback = self.dict.get("secondaryhold")
        elif event.button == Gdk.BUTTON_MIDDLE:
            callback = self.dict.get("onmiddleclick")
        else:
            callback = None

        if callback:
            self.__clasif_args(widget=widget, event=event, callback=callback)

    def __release_event(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            callback = self.dict.get("primaryrelease")

        elif event.button == Gdk.BUTTON_SECONDARY:
            callback = self.dict.get("secondaryrelease")
        else:
            callback = None

        if callback:
            self.__clasif_args(widget=widget, event=event, callback=callback)

    def __enter_event(self, widget, event):
        callback = self.dict.get("onhover")
        if callback:
            self.__clasif_args(widget=widget, event=event, callback=callback)

    def __leave_event(self, widget, event):
        callback = self.dict.get("onhoverlost")

        if callback:
            self.__clasif_args(widget=widget, event=event, callback=callback)

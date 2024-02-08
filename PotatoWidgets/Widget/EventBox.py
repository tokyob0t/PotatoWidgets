from ..Imports import *
from .Common import BasicProps, Events
from ..Variable import Listener, Poll, Variable


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
        attributes=lambda self: self,
        size=[0],
        css="",
        classname="",
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        visible=True,
    ):
        Gtk.EventBox.__init__(self)

        BasicProps.__init__(
            self,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=True,
            visible=visible,
            classname=classname,
            size=size,
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

    # Classification
    def __clasif_args(self, widget, event, callback):
        arg_num = callback.__code__.co_argcount
        arg_tuple = callback.__code__.co_varnames[:arg_num]

        if arg_num == 2:
            callback(widget=widget, event=event)
        elif arg_num == 1:
            if "widget" in arg_tuple and widget:
                callback(widget=widget)
            elif "event" in arg_tuple and event:
                callback(event=event)
            else:
                callback(event)
        else:
            callback()

    # def __click_event(self, _):
    #     callback = self.dict.get("onclick", None)
    #     if callback:
    #         self.__clasif_args(self, None, callback)

    def __clasif_scroll(self, widget, event):
        if event == Gdk.ScrollDirection.UP:
            callback = self.dict.get("onscrollup", None)
        elif event == Gdk.ScrollDirection.DOWN:
            callback = self.dict.get("onscrolldown", None)
        else:
            callback = None

        if callback:
            self.__clasif_args(widget, event, callback)

    def __press_event(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            callback = self.dict.get("primaryhold", None)
        elif event.button == Gdk.BUTTON_SECONDARY:
            callback = self.dict.get("secondaryhold", None)
        elif event.button == Gdk.BUTTON_MIDDLE:
            callback = self.dict.get("onmiddleclick", None)
        else:
            callback = None

        if callback:
            self.__clasif_args(widget, event, callback)

    def __release_event(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            callback = self.dict.get("primaryrelease", None)
        elif event.button == Gdk.BUTTON_SECONDARY:
            callback = self.dict.get("secondaryrelease", None)
        else:
            callback = None

        if callback:
            self.__clasif_args(widget, event, callback)

    def __enter_event(self, widget, event):
        callback = self.dict.get("onhover", None)
        if callback:
            self.__clasif_args(widget, event, callback)

    def __leave_event(self, widget, event):
        callback = self.dict.get("onhoverlost", None)
        if callback:
            self.__clasif_args(widget, event, callback)

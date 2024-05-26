from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps, Events


class EventBox(Gtk.EventBox, Events, BasicProps):
    def __init__(
        self,
        children: Union[Gtk.Widget, None] = None,
        onclick: Union[Callable, None] = None,
        onmiddleclick: Union[Callable, None] = None,
        onhover: Union[Callable, None] = None,
        onhoverlost: Union[Callable, None] = None,
        primaryhold: Union[Callable, None] = None,
        primaryrelease: Union[Callable, None] = None,
        secondaryhold: Union[Callable, None] = None,
        secondaryrelease: Union[Callable, None] = None,
        onscrollup: Union[Callable, None] = None,
        onscrolldown: Union[Callable, None] = None,
        attributes=lambda self: self,
        size: Union[int, str, List[Union[int, str]]] = 0,
        css: str = "",
        classname: str = "",
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        visible: bool = True,
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

        match arg_num:

            case 2:
                callback(widget=widget, event=event)
            case 1:
                if "widget" in arg_tuple and widget:
                    callback(widget=widget)
                elif "event" in arg_tuple and event:
                    callback(event=event)
                else:
                    callback(event)
            case _:
                callback()

    # def __click_event(self, _):
    #     callback = self.dict.get("onclick", None)
    #     if callback:
    #         self.__clasif_args(self, None, callback)

    def __clasif_scroll(self, widget, event):
        match event:
            case Gdk.ScrollDirection.UP:
                callback = self.dict.get("onscrollup", None)
            case Gdk.ScrollDirection.DOWN:
                callback = self.dict.get("onscrolldown", None)
            case _:
                callback = None

        if callback:
            self.__clasif_args(widget, event, callback)

    def __press_event(self, widget, event):
        match event.button:
            case Gdk.BUTTON_PRIMARY:
                callback = self.dict.get("primaryhold", None)
            case Gdk.BUTTON_SECONDARY:
                callback = self.dict.get("secondaryhold", None)
            case Gdk.BUTTON_MIDDLE:
                callback = self.dict.get("onmiddleclick", None)
            case _:
                callback = None

        if callback:
            self.__clasif_args(widget, event, callback)

    def __release_event(self, widget, event):
        match event.button:
            case Gdk.BUTTON_PRIMARY:
                callback = self.dict.get("primaryrelease", None)
            case Gdk.BUTTON_SECONDARY:
                callback = self.dict.get("secondaryrelease", None)
            case _:
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

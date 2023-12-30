from ...__Import import *


class Events(Gtk.Widget):
    def __init__(
        self,
        onclick=None,
        onmiddleclick=None,
        onhover=None,
        onhoverlost=None,
        primaryhold=None,
        primaryrelease=None,
        secondaryhold=None,
        secondaryrelease=None,
    ):
        super().__init__()

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

        self.connect("clicked", self.__click_event)
        self.connect("button-press-event", self.__press_event)
        self.connect("button-release-event", self.__release_event)
        self.connect("enter-notify-event", self.__enter_event)
        self.connect("leave-notify-event", self.__leave_event)

    def __click_event(self, _):
        # print("Click")
        callback = self.dict.get("onclick", None)
        if callback:
            callback()

    def __press_event(self, _, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            # print("Click PRIMARIO - Clickeado")
            callback = self.dict.get("primaryhold", None)
            if callback:
                callback()
        elif event.button == Gdk.BUTTON_SECONDARY:
            # print("Click SECUNDARIO - Clickeado")
            callback = self.dict.get("secondaryhold", None)
            if callback:
                callback()
        elif event.button == Gdk.BUTTON_MIDDLE:
            # print("Click MEDIO - Clickeado")
            callback = self.dict.get("onmiddleclick", None)
            if callback:
                callback()

    def __release_event(self, _, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            # print("Click PRIMARIO - Soltado")
            callback = self.dict.get("primaryrelease", None)
            if callback:
                callback()
        elif event.button == Gdk.BUTTON_SECONDARY:
            # print("Click SECUNDARIO - Soltado")
            callback = self.dict.get("secondaryrelease", None)
            if callback:
                callback()
            # elif event.button == Gdk.BUTTON_MIDDLE:
        # print("Click MEDIO - Soltado")

    def __enter_event(self, *args):
        # print("Hover")
        callback = self.dict.get("onhover", None)
        if callback:
            callback()

    def __leave_event(self, *args):
        # print("Hover lost")
        callback = self.dict.get("onhoverlost", None)
        if callback:
            callback()

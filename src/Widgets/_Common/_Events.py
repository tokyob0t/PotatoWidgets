from ...__Import import *


class Events(Gtk.Widget):
    def __init__(
        self,
        onclick,
        onmiddleclick,
        onhover,
        onhoverlost,
        primaryhold,
        primaryrelease,
        secondaryhold,
        secondaryrelease,
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

        self.connect("button-press-event", self.__press_event)
        self.connect("button-release-event", self.__release_event)
        self.connect("enter-notify-event", self.__enter_event)
        self.connect("leave-notify-event", self.__leave_event)

    def __click_event(self, _):
        # print("Click")
        if self.dict.get("onclick"):
            self.dict["onclick"]()

    def __press_event(self, _, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            # print("Click PRIMARIO - Clickeado")
            if self.dict.get("primaryhold"):
                self.dict["primaryhold"]()
        elif event.button == Gdk.BUTTON_SECONDARY:
            # print("Click SECUNDARIO - Clickeado")
            if self.dict.get("secondaryhold"):
                self.dict["secondaryhold"]()
        elif event.button == Gdk.BUTTON_MIDDLE:
            # print("Click MEDIO - Clickeado")
            if self.dict.get("onmiddleclick"):
                self.dict["onmiddleclick"]()

    def __release_event(self, _, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            # print("Click PRIMARIO - Soltado")
            if self.dict.get("primaryrelease"):
                self.dict["primaryrelease"]()
        elif event.button == Gdk.BUTTON_SECONDARY:
            # print("Click SECUNDARIO - Soltado")
            if self.dict.get("secondaryrelease"):
                self.dict["secondaryrelease"]()
            # elif event.button == Gdk.BUTTON_MIDDLE:
        # print("Click MEDIO - Soltado")

    def __enter_event(self, *args):
        # print("Hover")
        if self.dict.get("onhover"):
            self.dict["onhover"]()

    def __leave_event(self, *args):
        # print("Hover lost")
        if self.dict.get("onhoverlost"):
            self.dict["onhoverlost"]()

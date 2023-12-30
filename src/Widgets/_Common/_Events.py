from ...__Import import *

class Events(Gtk.Widget):
    def __init__(self,
                onclick,
                onmiddleclick,
                onhover,
                onhoverlost,
                primaryhold,
                primaryrelease,
                secondaryhold,
                secondaryrelease 
                ):
        self.dict = {
                "onclick":  onclick,
                "onmiddleclick": onmiddleclick,
                "onhover":  onhover,
                "onhoverlost":  onhoverlost,
                "primaryhold":  primaryhold,
                "primaryrelease": primaryrelease,
                "secondaryhold":  secondaryhold,
                "secondaryrelease": secondaryrelease
                }

        self.connect("clicked", self.__click_event)
        self.connect("button-press-event", self.__press_event)
        self.connect("button-release-event", self.__release_event)
        self.connect("enter-notify-event", self.__enter_event)
        self.connect("leave-notify-event", self.__leave_event)
        

    def __click_event(self, _):
        # print("Click")
        self.dict.get("onclick")
        print(self.dict.get("onclick"))
        
    def __press_event(self, _, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            # print("Click PRIMARIO - Clickeado")
            self.dict.get("primaryrelease")

        elif event.button == Gdk.BUTTON_SECONDARY:
            # print("Click SECUNDARIO - Clickeado")
            self.dict.get("secondaryrelease")

        elif event.button == Gdk.BUTTON_MIDDLE:
            self.dict.get("onmiddleclick")
            # print("Click MEDIO - Clickeado")
        

    def __release_event(self, _, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            print("Click PRIMARIO - Soltado")
            self.dict.get("")

        elif event.button == Gdk.BUTTON_SECONDARY:
            print("Click SECUNDARIO - Soltado")
        elif event.button == Gdk.BUTTON_MIDDLE:
            print("Click MEDIO - Soltado")
        

    def __enter_event(self, *args):
        print("Hover")
        

    def __leave_event(self, *args):
        print("Hover lost")
    
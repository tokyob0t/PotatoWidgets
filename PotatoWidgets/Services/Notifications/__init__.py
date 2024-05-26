from ..._Logger import Logger
from ...Env import DIR_CACHE_NOTIF_IMAGES, FILE_CACHE_NOTIF
from ...Imports import *
from ...Methods import idle, make_async, parse_interval, wait
from ..Service import BaseGObjectClass, Service

#
# Notification Structure
#
# notify-send -a "github" "Welcome to my setup" "This is a notification using potato, very cool huh?" -A Id_0=Pretty_Text -t 2000
#
# {
#    "name": "github",
#    "id": 10,
#    "image": "",
#    "summary": "Welcome to my setup",
#    "body": "This is a notification using potato, very cool huh?",
#    "urgency": "normal",
#    "actions": [{"id": "Id_0", "label": "Pretty_Text"}],
#    "hints": {"urgency": 1, "sender-pid": 23898},
#    "timeout": 2000,
# }

org_freedesktop_Notifications_xml = """
<?xml version="1.0" encoding="UTF-8"?>
<node>
   <interface name="org.freedesktop.Notifications">
      <method name="Notify">
         <arg name="Name" type="s" direction="in" />
         <arg name="Id" type="u" direction="in" />
         <arg name="Image" type="s" direction="in" />
         <arg name="Summary" type="s" direction="in" />
         <arg name="Body" type="s" direction="in" />
         <arg name="Actions" type="as" direction="in" />
         <arg name="Hints" type="a{sv}" direction="in" />
         <arg name="Timeout" type="i" direction="in" />
         <arg name="Notification_id" type="u" direction="out" />
      </method>
      <method name="GetServerInformation">
         <arg name="Name" type="s" direction="out" />
         <arg name="Vendor" type="s" direction="out" />
         <arg name="Version" type="s" direction="out" />
         <arg name="Spec_Version" type="s" direction="out" />
      </method>
      <method name="GetCapabilities">
         <arg name="Capabilities" type="as" direction="out" />
      </method>
      <method name="InvokeAction">
         <arg name="Id" type="u" direction="in" />
         <arg name="Action" type="s" direction="in" />
      </method>
      <signal name="ActionInvoked">
         <arg name="Id" type="u" />
         <arg name="Action" type="s" />
      </signal>
      <method name="CloseNotification">
         <arg name="Id" type="u" direction="in" />
      </method>
      <signal name="NotificationClosed">
         <arg name="Id" type="u" />
         <arg name="Reason" type="u" />
      </signal>
   </interface>
</node>
"""

NodeInfo = Gio.DBusNodeInfo.new_for_xml(org_freedesktop_Notifications_xml)


class Notification(BaseGObjectClass):
    __gsignals__ = Service.signals(
        {
            "dismiss": [],
            "closed": [],
            "action": [[str]],
        }
    )

    __gproperties__ = Service.properties({})

    def __init__(
        self,
        name: str,
        id: int,
        image: str,
        summary: str,
        body: str,
        actions: list,
        urgency: str,
        hints: Dict[str, Any],
        timeout: int,
    ) -> None:
        super().__init__()

        self._id: int = int(id)
        self._name: str = str(name)
        self._image: str = str(image)
        self._summary: str = str(summary)
        self._body: str = str(body)
        self._actions: list = list(actions)
        self._urgency: str = str(urgency)
        self._timeout: int = int(timeout)

        self._hints: Dict[str, Any] = dict(hints)

        if "image-data" in self._hints:
            del self._hints["image-data"]

    def bind(
        self,
        signal: Literal["dismiss", "close", "action"],
        format: Callable = lambda value: value,
    ):
        return super().bind(signal, format)

    def dismiss(self) -> None:
        self.emit("dismiss")

    def close(self) -> None:
        self.emit("closed")

    def action(self, action: str) -> None:
        self.emit("action", action)

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def image(self) -> str:
        return self._image

    @property
    def summary(self) -> str:
        return self._summary

    @property
    def body(self) -> str:
        return self._body

    @property
    def actions(self) -> list:
        return self._actions

    @property
    def urgency(self) -> str:
        return self._urgency

    @property
    def hints(self) -> Dict[str, Any]:
        return self._hints

    @property
    def timeout(self) -> int:
        return self._timeout

    def json(self) -> dict:
        return {
            "name": self.name,
            "id": self.id,
            "image": self.image,
            "summary": self.summary,
            "body": self.body,
            "urgency": self.urgency,
            "actions": self.actions,
            "hints": self.hints,
            "timeout": self.timeout,
        }


class _NotificationsService(Service):

    __gproperties__ = Service.properties(
        {
            "notifications": [object],
            "popups": [object],
            "count": [int],
            "dnd": [bool],
        }
    )
    __gsignals__ = Service.signals(
        {
            "notified": [[int]],
            "dismissed": [[int]],
            "closed": [[int]],
            "popup": [[int]],
        }
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._json: Dict[str, Any] = self.__load_json()
        self._dnd: bool = self._json["dnd"]
        self._count: int = self._json["count"]
        self._notifications: List[Notification] = self._json["notifications"]
        self._popups: List[Notification] = []
        self._timeout: int = 4500
        self._connection: Gio.DBusConnection
        self.__register__()

    def bind(
        self,
        signal: Literal[
            "closed",
            "action",
            "notified",
            "dismissed",
            "popup",
            "count",
            "dnd",
            "notifications",
            "popups",
        ],
        format: Callable = lambda value: value,
    ):
        return super().bind(signal, format)

    def emit(
        self,
        signal_name: Literal[
            "closed",
            "action",
            "notified",
            "dismissed",
            "popup",
            "count",
            "dnd",
            "notifications",
            "popups",
        ],
        *args: Any,
        **kwargs: Any,
    ) -> Union[Any, None]:
        return super().emit(signal_name, *args, **kwargs)

    def __add_notif(self, notif: Notification) -> None:
        self._count += 1
        self.emit("count")
        self._popups.append(notif)
        self._notifications.append(notif)

        if not self.dnd:
            self.emit("popup", notif.id)
            self.emit("popups")

            if self.timeout > 0:
                wait(self.timeout, notif.dismiss)

        self.emit("notified", notif.id)
        self.emit("notifications")

        notif.connect("dismiss", self.__on_dismiss)
        notif.connect("closed", self.__on_close)
        notif.connect("action", self.__on_action)

    def __on_action(self, notif: Notification, action: str) -> None:
        self.InvokeAction(notif.id, action)


    def __on_dismiss(self, notif: Notification) -> None:
        if notif in self._popups:
            self.emit("dismissed", notif.id)
            self.emit("popups")
            del self._popups[self._popups.index(notif)]

    def __on_close(self, notif: Notification) -> None:

        if notif in self._popups:
            self.emit("dismissed", notif.id)
            self.emit("popups")
            del self._popups[self._popups.index(notif)]

        if notif in self._notifications:
            self._count -= 1
            self.emit("closed", notif.id)
            self.emit("count")
            del self._notifications[self._notifications.index(notif)]

        self.CloseNotification(notif.id)

    #
    #
    #
    #
    #

    @property
    def count(self) -> int:
        return self._count

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, new_timeout: Union[str, int]) -> None:
        new_timeout = parse_interval(new_timeout)
        if new_timeout > 0:
            self._timeout = new_timeout
        else:
            self._timeout = 4500

    @property
    def dnd(self) -> bool:
        return self._dnd

    @dnd.setter
    def dnd(self, new_value: bool) -> None:
        self._dnd = new_value
        self.emit("dnd")

    @property
    def notifications(self) -> List[Notification]:
        return self._notifications

    @property
    def popups(self) -> List[Notification]:
        return self._popups

    def get_popup(self, id: int) -> Union[Notification, None]:
        return next((i for i in self._popups if i.id == id), None)

    def get_notification(self, id: int) -> Union[Notification, None]:
        return next((i for i in self._notifications if id == i.id), None)

    def get_notifications(self) -> List[Notification]:
        return self.notifications

    def get_popups(self) -> List[Notification]:
        return self.popups

    @make_async
    def clear(self) -> None:
        if not self.notifications:
            return

        for notif in self._notifications[::]:
            if notif in self._popups:
                self.emit("dismissed", notif.id)

            if notif in self._notifications:
                self.emit("closed", notif.id)
            self.CloseNotification(notif.id)

        self._count = 0
        self._notifications = []
        self._popups = []

        self.__save_json()
        self.emit("count")
        self.emit("notifications")
        self.emit("popups")

    def __load_json(
        self,
    ) -> Dict[str, Union[bool, int, List[None], List[Notification]]]:
        try:
            with open(FILE_CACHE_NOTIF, "r") as file:
                data = json.load(file)

            return_data = {
                "dnd": False,
                "count": 0,
                "notifications": [],
            }

            return_data["dnd"] = data.get("dnd", False)
            return_data["count"] = data.get("count", 0)
            return_data["notifications"] = [
                Notification(
                    id=i["id"],
                    name=i["name"],
                    image=i["image"],
                    summary=i["summary"],
                    body=i["body"],
                    urgency=i["urgency"],
                    actions=i["actions"],
                    hints=i["hints"],
                    timeout=i["timeout"],
                )
                for i in data.get("notifications", [])
            ]
            return return_data

        except json.decoder.JSONDecodeError:
            return {
                "dnd": False,
                "count": 0,
                "notifications": [],
            }

    def __save_json(self) -> None:
        data = {
            "dnd": self.dnd,
            "count": self.count,
            "notifications": [i.json() for i in self.notifications],
        }

        with open(FILE_CACHE_NOTIF, "w") as file:
            json.dump(data, file)

    #
    # Other
    #

    def __get_id(self, new_id) -> int:
        if new_id != 0:
            return new_id
        else:
            notifs = self.notifications
            if notifs and notifs[-1]:
                return notifs[-1].id + 1
            else:
                return 1

    def __get_urgency(self, hints: Dict[str, Any]) -> str:
        return {0: "low", 1: "normal", 2: "critical"}.get(
            hints.get("urgency", 0), "low"
        )

    def __get_actions(self, actions: List[str]) -> List[Union[Dict[str, str], None]]:
        return [
            {
                "id": actions[i],
                "label": actions[i + 1],
            }
            for i in range(0, len(actions), 2)
        ]

    def __decode_icon(self, hints: Dict[str, Any], id: int) -> str:
        _hint: Union[list, None] = hints.get("image-data")

        if _hint:
            image_path: str = f"{DIR_CACHE_NOTIF_IMAGES}/{id}.png"

            self.__save_icon_async(_hint, image_path)

            return image_path

        return ""

    @make_async
    def __save_icon_async(self, _hint, image_path) -> None:
            GdkPixbuf.Pixbuf.new_from_bytes(
                data=GLib.Bytes(_hint[6]),
                colorspace=GdkPixbuf.Colorspace.RGB,
                has_alpha=_hint[3],
                bits_per_sample=_hint[4],
                width=_hint[0],
                height=_hint[1],
                rowstride=_hint[2],
            ).savev(image_path, "png")

    ## Dbus Methods-Signals and that stuff

    #
    # Pair Method-Signal
    #

    def CloseNotification(self, id: int, reason:int=3) -> None:
        self.NotificationClosed(id, reason)

    def NotificationClosed(self, id: int, reason: int) -> None:
        self._connection.emit_signal(
            "org.freedesktop.Notifications",
            "/org/freedesktop/Notifications",
            "org.freedesktop.Notifications",
            "NotificationClosed",
            GLib.Variant("(uu)", (id, reason)),
        )

    def InvokeAction(self, id: int, action: str) -> None:
        self.ActionInvoked(id, action)

    def ActionInvoked(self, id: int, action: str) -> None:
        self._connection.emit_signal(
            "org.freedesktop.Notifications",
            "/org/freedesktop/Notifications",
            "org.freedesktop.Notifications",
            "ActionInvoked",
            GLib.Variant("(us)", (id, action)),
        )

    def GetServerInformation(self) -> GLib.Variant:
        return GLib.Variant(
            "(ssss)",
            (
                "Potato Notification Daemon",
                "t0kyob0y",
                "0.1",
                "1.2"
            )
        )

    def GetCapabilities(self) -> GLib.Variant:
        return GLib.Variant(
            "(as)",
            (
                (
                    "action-icons",
                    "actions",
                    "body",
                    "body-hyperlinks",
                    "body-markup",
                    "icon-static",
                    "persistence",
                ),
            ),
        )

    def Notify(
        self,
        name: str,
        id: int,
        image: str,
        summary: str,
        body: str,
        actions: List[str],
        hints: Dict[str, Any],
        timeout: int,
    ) -> GLib.Variant:

        _id: int = self.__get_id(id)
        _urgency: str = self.__get_urgency(hints)
        _actions: list = self.__get_actions(actions)
        _image: str = image or self.__decode_icon(hints, id)

        notif = Notification(
            name=name,
            id=_id,
            image=_image,
            urgency=_urgency,
            summary=summary,
            body=body,
            actions=_actions,
            hints=hints,
            timeout=timeout,
        )

        self.__add_notif(notif) 
        self.__save_json()
        return GLib.Variant("(u)", (notif.id,))

    ## DBus Stuff

    def __register__(self) -> None:
        # https://lazka.github.io/pgi-docs/index.html#Gio-2.0/functions.html#Gio.bus_own_name
        Gio.bus_own_name(
            Gio.BusType.SESSION,  # Bus_Type
            "org.freedesktop.Notifications",  # Name
            Gio.BusNameOwnerFlags.DO_NOT_QUEUE,  # Flags
            self.__on_success__,  # bus_acquired_closure
            None,  # name_acquired_closure
            self.__on_failed__,  # name_lost_closure
        )

    def __on_success__(
        self,
        Connection: Gio.DBusConnection,
        BusName: Literal["org.freedesktop.Notifications"],
    ):
        self._connection = Connection
        Connection.register_object(
            "/org/freedesktop/Notifications",
            NodeInfo.interfaces[0],
            self.__on_call__,
        )

    def __on_failed__(
        self,
        Connection: Gio.DBusConnection,
        BusName: Literal["org.freedesktop.Notifications"],
    ):
        Name = Connection.call_sync(
            bus_name=BusName,
            object_path="/org/freedesktop/Notifications",
            interface_name=BusName,
            method_name="GetServerInformation",
            parameters=GLib.Variant("()", ()),
            reply_type=GLib.VariantType.new("(ssss)"),
            flags=Gio.DBusCallFlags.NONE,
            timeout_msec=-1,
        )

        Logger.ERROR("There is already a notifications daemon running:", *Name)

    def __on_call__(
        self,
        Connection: Gio.DBusConnection,
        Sender: str,
        Path: Literal["/org/freedesktop/Notifications"],
        BusName: Literal["org.freedesktop.Notifications"],
        Method: str,
        Parameters: tuple,
        MethodInvocation: Gio.DBusMethodInvocation,
    ):
        try:
            match Method:
                case "GetServerInformation":
                    MethodInvocation.return_value(self.GetServerInformation())
                case "GetCapabilities":
                    MethodInvocation.return_value(self.GetCapabilities())
                case "Notify":
                    MethodInvocation.return_value(self.Notify(*Parameters))
                case "CloseNotification":
                    MethodInvocation.return_value(self.CloseNotification(*Parameters))
                case "InvokeAction":
                    MethodInvocation.return_value(self.InvokeAction(*Parameters))
                case _:
                    print("Cllback no llamado", Method, Parameters)
        except Exception as r:
            Logger.ERROR(r)
        #finally:
        #    return Connection.flush()


NotificationsService = _NotificationsService()

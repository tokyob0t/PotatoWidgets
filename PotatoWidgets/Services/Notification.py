from ..Imports import *
from ..Methods import lookup_icon, parse_interval, wait
from .Service import *


class Notification(ServiceChildren):
    __gsignals__ = {
        "dismiss": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "close": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "action": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

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

        if "image-data" in dict(hints):
            del hints["image-data"]

        self._hints: Dict[str, Any] = dict(hints)

    def bind(
        self,
        signal: Literal["dismiss", "close", "action"],
        initial_value: Any = 0,
    ):
        return super().bind(signal, initial_value)

    def dismiss(self) -> None:
        self.emit("dismiss")

    def close(self) -> None:
        self.emit("close")

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

    def __str__(self) -> str:
        return str(self.json())

    def __repr__(self) -> str:
        return self.__str__()


class NotificationsService(Service):
    __gsignals__ = {
        "notified": (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        "dismissed": (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        "closed": (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        "popup": (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        "action": (GObject.SignalFlags.RUN_FIRST, None, (int, str)),
        "count": (GObject.SignalFlags.RUN_FIRST, None, (int,)),
    }

    def __init__(self) -> None:
        super().__init__()
        self._json: Dict[str, Any] = self._load_json()
        self._count: int = self._json["count"]
        self._popups: List[Union[Notification, None]] = self._json["popups"]
        self._notifications: List[Union[Notification, None]] = self._json[
            "notifications"
        ]
        self._dnd: bool = False
        self._timeout: int = 4500
        self._sort_all()

    def bind(
        self,
        signal: Literal[
            "notified",
            "dismissed",
            "closed",
            "popup",
            "action",
            "count",
        ],
        initial_value: Any = 0,
    ):
        return super().bind(signal, initial_value)

    def _add_notif(self, notif: Notification) -> None:
        self._count += 1
        self._notifications.append(notif)
        self._popups.append(notif)

        if not self.dnd:
            self.emit("popup", notif.id)

        self.emit("notified", notif.id)
        self.emit("count", self.count)

        notif.connect("dismiss", self._on_dismiss)
        notif.connect("close", self._on_close)
        notif.connect("action", self._on_action)

        if self.timeout > 0:
            _ = wait(self.timeout, notif.dismiss)

        self._save_json()

    def _on_close(self, notif: Notification) -> None:
        if notif in self.popups:
            self._popups.remove(notif)
        if notif in self.notifications:
            self._count -= 1
            self._notifications.remove(notif)
            self.emit("closed", notif.id)
            self.emit("count", self.count)

    def _on_action(self, notif: Notification, action: str) -> None:
        self.emit("action", notif.id, action)

    def _on_dismiss(self, notif: Notification) -> None:
        if notif in self.popups:
            self._popups.remove(notif)
            self.emit("dismissed", notif.id)

    @property
    def count(self) -> int:
        return self._count

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, new_timeout: Union[str, int]) -> None:
        self._timeout = parse_interval(new_timeout)

    def set_timeout(self, new_timeout: Union[str, int]) -> None:
        self.timeout = new_timeout

    def get_timeout(self) -> int:
        return self.timeout

    @property
    def dnd(self) -> bool:
        return self._dnd

    @dnd.setter
    def dnd(self, new_value: bool) -> None:
        self._dnd = new_value

    def get_dnd(self) -> bool:
        return self.dnd

    def set_dnd(self, new_value: bool) -> None:
        self.dnd = new_value

    @property
    def notifications(self) -> List[Union[Notification, None]]:
        return self._notifications

    @property
    def popups(self) -> List[Union[Notification, None]]:
        return self._popups

    def get_popup(self, id: int) -> Union[Notification, None]:
        return self._search(self._popups, id)

    def get_notification(self, id: int) -> Union[Notification, None]:
        return self._search(self._notifications, id)

    def get_notifications(self) -> List[Union[Notification, None]]:
        return self._notifications

    def get_popups(self) -> List[Union[Notification, None]]:
        return self._popups

    def _sort_all(self) -> None:
        if self.notifications:
            self._sort(self._notifications)
        if self.popups:
            self._sort(self._popups)

    def _search(
        self, array: List[Union[Notification, None]], target_id: int
    ) -> Union[Notification, None]:
        left, right = 0, len(array) - 1
        while left <= right:
            mid = (left + right) // 2
            if array[mid].id == target_id:
                return array[mid]
            elif array[mid].id < target_id:
                left = mid + 1
            else:
                right = mid - 1

    def _sort(self, array: List[Union[Notification, None]]) -> None:
        for i in range(1, len(array)):
            current = array[i]
            j = i - 1
            while j >= 0 and array[j].id > current.id:
                array[j + 1] = array[j]
                j -= 1
            array[j + 1] = current

    def clear(self) -> None:
        if self.notifications:
            for i in range(len(self.notifications)):
                notif = self._notifications[i]

                if notif:
                    wait(100 * notif.id, notif.close)

        self._count = 0
        self._notifications = []
        self._popups = []
        self.emit("count", self.count)
        self._save_json()

    def _load_json(
        self,
    ) -> Dict[str, Union[bool, int, List[None], List[Notification]]]:
        try:
            with open(FILE_CACHE_NOTIF, "r") as file:
                data = json.load(file)
                if data["popups"]:
                    data["popups"] = []
                if data["notifications"]:
                    data["notifications"] = [
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
                        for i in data["notifications"]
                    ]
                return data

        except json.decoder.JSONDecodeError:
            return {
                "dnd": False,
                "count": 0,
                "popups": [],
                "notifications": [],
            }

    def _save_json(self) -> None:
        data = {
            "dnd": self.dnd,
            "count": self.count,
            "popups": [],
            "notifications": [i.json() for i in self.notifications if i],
        }

        with open(FILE_CACHE_NOTIF, "w") as file:
            json.dump(data, file)


class NotificationsDbusService(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName(
            "org.freedesktop.Notifications", bus=dbus.SessionBus()
        )
        super().__init__(bus_name, "/org/freedesktop/Notifications")
        NotificationsService().connect(
            "closed", lambda _, id: self.NotificationClosed(id, 2)
        )
        NotificationsService().connect(
            "action", lambda _, id, action_id: self.InvokeAction(id, action_id)
        )

    #
    # Methods
    #
    @dbus.service.method(
        "org.freedesktop.Notifications", in_signature="", out_signature="ssss"
    )
    def GetServerInformation(self):
        return ("Potato Notification Daemon", "t0kyob0y", "0.1", "1.2")

    @dbus.service.method(
        "org.freedesktop.Notifications", in_signature="", out_signature="as"
    )
    def GetCapabilities(self):
        return (
            "action-icons",
            "actions",
            "body",
            "body-hyperlinks",
            "body-markup",
            "icon-static",
            "persistence",
        )

    @dbus.service.method(
        "org.freedesktop.Notifications", in_signature="susssasa{sv}i", out_signature="u"
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
    ) -> int:
        _id: int = self._get_id(id)
        _urgency: str = self._get_urgency(hints)
        _actions: list = self._get_actions(actions)
        _image: str = image or self._get_image(hints, id)

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

        NotificationsService()._add_notif(notif)
        return _id

    @dbus.service.method(
        "org.freedesktop.Notifications", in_signature="us", out_signature=""
    )
    def InvokeAction(self, id: int, action: str) -> None:
        self.ActionInvoked(id, action)

    #
    # Signals
    #

    @dbus.service.signal("org.freedesktop.Notifications", signature="us")
    def ActionInvoked(self, id: int, action: str) -> Tuple[int, str]:
        return (id, action)

    @dbus.service.signal("org.freedesktop.Notifications", signature="uu")
    def NotificationClosed(self, id: int, reason: int = 2) -> Tuple[int, int]:
        return (id, reason)

    def _get_id(self, new_id) -> int:
        if new_id != 0:
            return new_id
        else:
            notifs = NotificationsService().notifications
            if notifs and notifs[-1]:
                return notifs[-1].id + 1
            else:
                return 1

    def _get_urgency(self, hints: Dict[str, Any]) -> str:
        _hint: int = hints.get("urgency", 0)
        return {0: "low", 1: "normal", 2: "critical"}.get(_hint, "low")

    def _get_actions(self, actions: List[str]) -> List[Union[Dict[str, str], None]]:
        return [
            {
                "id": actions[i],
                "label": actions[i + 1],
            }
            for i in range(0, len(actions), 2)
        ]

    # Other Methods
    def _get_image(self, hints: Dict[str, Any], id: int) -> str:
        _hint: Union[list, None] = hints.get("image-data")

        if _hint is not None:
            image_path: str = f"{DIR_CACHE_NOTIF_IMAGES}/{id}.png"

            GdkPixbuf.Pixbuf.new_from_bytes(
                width=_hint[0],
                height=_hint[1],
                rowstride=_hint[2],
                has_alpha=_hint[3],
                bits_per_sample=_hint[4],
                data=GLib.Bytes(_hint[6]),
                colorspace=GdkPixbuf.Colorspace.RGB,
            ).savev(image_path, "png")

            return image_path

        return ""

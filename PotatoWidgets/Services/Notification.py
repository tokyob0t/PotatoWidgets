from ..Imports import *
from ..Methods import lookup_icon, parse_interval, wait
from .Service import *


class Notification(GObject.Object):
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
        self._hints: Dict[str, Any] = dict(hints)
        self._timeout: int = int(timeout)

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
        "action": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (int, str),
        ),
    }

    def __init__(self) -> None:
        super().__init__()
        self._json: Dict[str, Any] = self._load_json()
        self._count: int = 0
        self._popups: List[Union[Notification, None]] = self._json["popups"]
        self._notifications: List[Union[Notification, None]] = self._json[
            "notifications"
        ]
        self._dnd: bool = False
        self._timeout: int = 4500
        self._sort_all()

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, new_timeout: Union[str, int]) -> None:
        self._timeout = parse_interval(new_timeout)

    @property
    def dnd(self) -> bool:
        return self._dnd

    @dnd.setter
    def dnd(self, new_value: bool) -> None:
        if self.dnd != new_value:
            self._dnd = new_value
            self.emit("dnd", self.dnd)

    @property
    def notifications(self) -> List[Union[Notification, None]]:
        return self._notifications

    @property
    def popups(self) -> List[Union[Notification, None]]:
        return self._popups

    def close_notification(self, id: int) -> None:
        _n = self.get_notification(id)
        if _n:
            _n.close()

    def dismiss_notification(self, id: int) -> None:
        _n = self.get_notification(id)
        if _n:
            _n.dismiss()

    def action_notification(self, id: int, action_id: str) -> None:
        _n = self.get_notification(id)
        if _n:
            _n.action(action_id)

    def get_popup(self, id: int) -> Union[Notification, None]:
        return self._search(self._popups, id)

    def get_notification(self, id: int) -> Union[Notification, None]:
        return self._search(self._notifications, id)

    def get_notifications(self) -> List[Union[Notification, None]]:
        return self._notifications

    def get_popups(self) -> List[Union[Notification, None]]:
        return self._popups

    def _load_json(self) -> Dict[str, Union[bool, List[Union[Notification, None]]]]:
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
                "popups": [],
                "notifications": [],
            }

    def _save_json(self) -> None:
        data = {
            "dnd": self.dnd,
            "popups": [i.json() for i in self.popups if i],
            "notifications": [i.json() for i in self.notifications if i],
        }

        with open(FILE_CACHE_NOTIF, "w") as file:
            json.dump(data, file, indent=1)

    def _sort_all(self) -> None:
        if self.notifications:
            self._sort(self._notifications)
        if self.popups:
            self._sort(self._popups)

    def _add_notif(self, notif: Notification) -> None:
        self._notifications.append(notif)
        self._popups.append(notif)

        if not self.dnd:
            self.emit("popup", notif.id)
            self.notify("popups")

        self.emit("notified", notif.id)
        notif.connect("dismiss", lambda instance: self.emit("dismissed", instance.id))
        notif.connect("close", lambda instance: self.emit("closed", instance.id))
        notif.connect(
            "action",
            lambda instance, action_id: self.emit("action", instance.id, action_id),
        )

        if self.timeout > 0:
            wait(self.timeout, notif.dismiss)

        self._save_json()

    def _close_notif(self, id: int) -> None:
        _n_pop = self.get_popup(id)
        _n_notif = self.get_notification(id)

        if _n_pop:
            wait(100 * id, lambda: self._popups.remove(_n_pop))
        if _n_notif:
            wait(100 * id, lambda: self._notifications.remove(_n_notif))

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
            for i in range(len(self._notifications)):
                notif = self._notifications[i]

                if notif:
                    wait(100 * notif.id, notif.close)

        self._notifications = []
        self._popups = []

        self._save_json()


class NotificationsDbusService(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName(
            "org.freedesktop.Notifications", bus=dbus.SessionBus()
        )
        super().__init__(bus_name, "/org/freedesktop/Notifications")
        self._instance = NotificationsService()

        self._instance.connect(
            "action", lambda _, id, action_id: self.InvokeAction(id, action_id)
        )
        self._instance.connect("closed", lambda _, id: self.NotificationClosed(id, 2))

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
        _image: str = self._decode_image(image, hints, id)

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

        self._instance._add_notif(notif)
        return _id

    @dbus.service.signal("org.freedesktop.Notifications", signature="us")
    def ActionInvoked(self, id: int, action: str) -> Tuple[int, str]:
        return (id, action)

    @dbus.service.method(
        "org.freedesktop.Notifications", in_signature="us", out_signature=""
    )
    def InvokeAction(self, id: int, action: str) -> None:
        self.ActionInvoked(id, action)

    @dbus.service.signal("org.freedesktop.Notifications", signature="uu")
    def NotificationClosed(self, id: int, reason: int) -> Tuple[int, int]:
        return (id, reason)

    def _decode_image(self, app_image: str, hints: dict, notification_id: int) -> str:
        if app_image.startswith("file://") or GLib.file_test(
            app_image, GLib.FileTest.EXISTS
        ):
            return app_image

        if app_image:
            return app_image

        if "image-data" in hints:
            image_data = hints["image-data"]
            image_path = f"{DIR_CACHE_NOTIF_IMAGES}/{notification_id}"

            GdkPixbuf.Pixbuf.new_from_bytes(
                width=image_data[0],
                height=image_data[1],
                has_alpha=image_data[3],
                data=GLib.Bytes(image_data[6]),
                colorspace=GdkPixbuf.Colorspace.RGB,
                rowstride=image_data[2],
                bits_per_sample=image_data[4],
            ).savev(image_path, "png")

            return image_path

        return ""

    def _get_id(self, new_id) -> int:
        id = (
            new_id
            if new_id != 0
            else (
                self._instance.notifications[-1].id + 1
                if self._instance.notifications
                else 1
            )
        )
        return id

    def _get_urgency(self, hints: dict) -> str:
        _hint: int = hints.get("urgency", 0)
        return {0: "low", 1: "normal", 2: "critical"}.get(_hint, "low")

    def _get_actions(self, actions: List[str]) -> List[Union[dict, None]]:
        return [
            {"id": str(actions[i]), "label": str(actions[i + 1])}
            for i in range(0, len(actions), 2)
        ]


NotificationsService()
NotificationsDbusService()

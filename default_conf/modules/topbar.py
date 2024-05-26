from datetime import datetime

from PotatoWidgets import Bash, Poll, Widget, interval
from PotatoWidgets.Services import BatteryService

from .utils import *

if Bash.get_env("HYPRLAND_INSTANCE_SIGNATURE"):
    print("hyprñand detected")

    from .hyprland import Workspaces
elif Bash.get_env("DESKTOP_SESSION") == "bspwm":
    print("bspwm detected")
    from .bspwm import Workspaces
else:

    def Workspaces():
        return []


def Brightness():
    icon = Widget.Icon("display-brightness-symbolic", 20)
    scale = Widget.Scale(
        onchange=lambda b: Bash.run_async(f"brightnessctl set {b}%"),
        value=BRIGHTNESS.value,
        valign="center",
        vexpand=True,
        css="min-width: 100px;",
    )

    interval("1s", lambda: scale.set_value(BRIGHTNESS.value))

    return [icon, scale]


def Volume():
    def get_icon(value: int) -> str:
        if value == 0:
            return "audio-volume-muted-symbolic"
        elif value < 30:
            return "audio-volume-low-symbolic"
        elif value < 60:
            return "audio-volume-medium-symbolic"
        else:
            return "audio-volume-high-symbolic"

    icon = Widget.Icon(get_icon(VOLUME.value), 20)
    icon.bind(VOLUME, lambda out: icon.set_icon(get_icon(out)))

    scale = Widget.Scale(
        attributes=lambda self: self.bind(VOLUME, self.set_value),
        value=VOLUME.value,
        valign="center",
        vexpand=True,
        css="min-width: 100px;",
        onchange=lambda v: Bash.run_async(f"pactl set-sink-volume @DEFAULT_SINK@ {v}%"),
    )

    return [icon, scale]


def Battery():
    icon = Widget.Icon(
        icon=BatteryService.bind("icon-name"),
        size=20,
    )
    progressbar = Widget.ProgressBar(BatteryService.bind("percentage"), valign="center")
    return [icon, progressbar]


def NotifIndicator():
    def wrapper(count: int):
        if count:
            return "user-available-symbolic"
        return "user-idle-symbolic"

    icon = Widget.Icon("user-available-symbolic", 20)
    label = Widget.Label(NotificationsService.bind("count"))

    NotificationsService.connect(
        "count", lambda _, count: icon.set_icon(wrapper(count))
    )

    return Widget.Button(
        Widget.Box([icon, label], spacing=10),
        onclick=lambda: NotificationsService.clear(),
    )


def Topbar():
    return Widget.Window(
        position="top left right",
        size=["100%", 50],
        children=Widget.CenterBox(
            css="background-color: #161616; padding: 0 20px;",
            start=NotifIndicator(),
            center=Widget.Box(
                spacing=10,
                children=Workspaces() + Volume() + Brightness() + Battery(),
            ),
            end=Widget.Box(
                children=Widget.Label(
                    text=Poll(
                        "1m", lambda: datetime.now().strftime("%H:%M %p  %d/%m/%Y")
                    )
                ),
            ),
        ),
    )


MyTopbar = Topbar()

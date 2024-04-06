import re

from PotatoWidgets import Bash, Gio, NotificationsService, Variable, Widget

VOLUME = Variable(0)
BRIGHTNESS = Variable(0)
NOTIFICATIONS = NotificationsService().bind("count")


def UpdateVolume(stdout: str) -> None:
    if "on sink" in stdout:
        volume_output = Bash.get_output("pactl get-sink-volume @DEFAULT_SINK@")
        volume_match = re.search(r"(\d+)%", volume_output)
        if volume_match:
            value = volume_match.group(0).strip("%")
            VOLUME.value = int(value)


def UpdateBrightness(
    _FileMonitor: Gio.FileMonitor, _File: Gio.File, _: None, Event: Gio.FileMonitorEvent
) -> None:
    if Event == Gio.FileMonitorEvent.CHANGED:
        output = Bash.get_output("brightnessctl")
        match = re.search(r"Current.*\((\d{1,3})%\)", output)
        value = 0
        if match is not None:
            value = int(match.group(1))
        if value != BRIGHTNESS.value:

            BRIGHTNESS.value = value


Bash.popen("pactl subscribe", stdout=UpdateVolume)


BRIGHTNESS_FILE = Bash.get_output("ls /sys/class/backlight").splitlines()[0]

BRIGHTNESS_MONITOR = Bash.monitor_file(
    f"/sys/class/backlight/{BRIGHTNESS_FILE}/brightness",
    flags="watch_moves",
)

BRIGHTNESS_MONITOR.connect("changed", UpdateBrightness)

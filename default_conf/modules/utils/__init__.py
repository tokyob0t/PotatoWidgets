from PotatoWidgets import Bash, NotificationsService, Variable

VOLUME = Variable(0)
BRIGHTNESS = Variable(0)
NOTIFICATIONS = NotificationsService().bind("count")


def UpdateVolume(_) -> None:
    volume = Bash.get_output(
        "pactl get-sink-volume @DEFAULT_SINK@ | grep -Po '[0-9]{1,3}(?=%)' | head -1",
        int,
    )
    if volume != VOLUME.value:
        VOLUME.value = int(volume)


def UpdateBrightness() -> None:
    brightness = Bash.get_output(
        "brightnessctl | grep Current | awk '{print $4}' | sed 's/[(%)]//g'",
        int,
    )
    if brightness != BRIGHTNESS.value:
        BRIGHTNESS.value = brightness


BRIGHTNESS_FILE = Bash.get_output("ls /sys/class/backlight", list)[0]

Bash.popen(
    """bash -c 'pactl subscribe | grep --line-buffered "on sink"' """,
    stdout=UpdateVolume,
)

Bash.monitor_file(
    f"/sys/class/backlight/{BRIGHTNESS_FILE}/brightness",
    flags="watch_moves",
    call_when=["changed"],
    callback=lambda: UpdateBrightness(),
)

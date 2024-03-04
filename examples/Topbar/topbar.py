#!/usr/bin/python

import subprocess
from os import getenv

from PotatoWidgets import Listener, Poll, PotatoLoop, Variable, Widget

if __name__ == "__main__":

    def get_volume():
        with subprocess.Popen(
            ["pactl", "subscribe"], stdout=subprocess.PIPE, text=True
        ) as proc:
            for line in proc.stdout:
                if "on sink" in line:
                    volume = subprocess.getoutput(
                        "pactl get-sink-volume @DEFAULT_SINK@ | grep -Po '[0-9]{1,3}(?=%)' | head -1"
                    )
                    yield volume

    def get_brightness():
        def get_value():
            return int(
                subprocess.getoutput("brightnessctl | grep Current | awk '{print $4}'")
                .replace("(", "")
                .replace(")", "")
                .replace("%", "")
            )

        with subprocess.Popen(
            [
                "inotifywait",
                "-m",
                "-e",
                "modify",
                f"/sys/class/backlight/{subprocess.getoutput('ls /sys/class/backlight/')}/brightness",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        ) as proc:
            for _ in proc.stdout:
                yield get_value()

    def hypr():
        SIGNATURE = getenv("HYPRLAND_INSTANCE_SIGNATURE")

        with subprocess.Popen(
            ["socat", "-u", f"UNIX-CONNECT:/tmp/hypr/{SIGNATURE}/.socket2.sock", "-"],
            stdout=subprocess.PIPE,
            text=True,
        ) as proc:
            for line in proc.stdout:
                line = line.replace("\n", "")
                if "activewindow>>" in line:
                    yield line.split(",")[1].capitalize()

    date = Poll(1000, lambda: subprocess.getoutput("date '+%b %d %I:%M:%S'"))
    volume = Listener(get_volume)
    brightness = Listener(get_brightness)
    activewindow = Listener(hypr)

    Topbar = Widget.EventBox(
        children=Widget.Box(
            valign="center",
            spacing=10,
            size=[0, 50],
            css="padding: 0 20px;",
            children=[
                Widget.Label(date),
                Widget.Label(
                    activewindow, hexpand=True, classname="labeltest horizontal"
                ),
                Widget.Label(
                    "volume: 0%",
                    attributes=lambda self: self.bind(
                        volume, lambda out: self.set_text(f"volume: {out}%")
                    ),
                ),
                Widget.Label(
                    "brightness: 0%",
                    attributes=lambda self: self.bind(
                        brightness, lambda out: self.set_text(f"brightness: {out}%")
                    ),
                ),
            ],
        ),
    )

    MyFirstWindow = Widget.Window(
        at={"top": "20px", "left": "20", "right": 20},  # You can use any
        size=[0, 20],  # even %
        position="top left right",
        exclusive=True,
        # focusable=True,
        # popup=True,
        children=Topbar,
    )

    MyFirstWindow.open()
    PotatoLoop()

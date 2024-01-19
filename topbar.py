#!/usr/bin/python

import subprocess
from datetime import datetime
from os import getenv

from PotatoWidgets import PotatoLoop, Variable, Widget

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

    date = Variable.Poll(1000, lambda: subprocess.getoutput("date '+%b %d %I:%M:%S'"))
    volume = Variable.Listener(get_volume)
    activewindow = Variable.Listener(hypr)

    Topbar = Widget.EventBox(
        children=Widget.Box(
            valign="center",
            spacing=10,
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
                Widget.Label().bind(volume, lambda self: self.set_text(volume)),
                Widget.Box(
                    [
                        Widget.ProgressBar(value=50, orientation="v"),
                        Widget.ProgressBar(value=50, orientation="v", inverted=True),
                    ]
                ),
                Widget.Box(
                    [
                        Widget.ProgressBar(value=50),
                        Widget.ProgressBar(value=50, inverted=True),
                    ],
                    orientation="v",
                    valign="center",
                ),
                Widget.Box(
                    [
                        Widget.Scale(value=50, orientation="v", size=[0, 100]),
                        Widget.Scale(
                            value=50, orientation="v", size=[0, 100], inverted=True
                        ),
                    ]
                ),
                Widget.Box(
                    [
                        Widget.Scale(value=50),
                        Widget.Scale(value=50, inverted=True),
                    ],
                    orientation="v",
                    valign="center",
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

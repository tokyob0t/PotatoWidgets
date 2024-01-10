#!/usr/bin/python

import subprocess
from datetime import datetime
from os import getenv

from PotatoWidgets import PotatoLoop, Variable, Widget

if __name__ == "__main__":

    def get_volume(self):
        with subprocess.Popen(
            ["pactl", "subscribe"], stdout=subprocess.PIPE, text=True
        ) as proc:
            for line in proc.stdout:
                if "on sink" in line:
                    volume = subprocess.getoutput(
                        "pactl get-sink-volume @DEFAULT_SINK@ | grep -Po '[0-9]{1,3}(?=%)' | head -1"
                    )
                    self.set_value(volume)

    def hypr(self):
        SIGNATURE = getenv("HYPRLAND_INSTANCE_SIGNATURE")

        with subprocess.Popen(
            ["socat", "-u", f"UNIX-CONNECT:/tmp/hypr/{SIGNATURE}/.socket2.sock", "-"],
            stdout=subprocess.PIPE,
            text=True,
        ) as proc:
            for line in proc.stdout:
                line = line.replace("\n", "")
                if "activewindow>>" in line:
                    self.set_value(line.split(",")[1].capitalize())

    date = Variable.Poll(1000, lambda: subprocess.getoutput("date '+%b %d %I:%M:%S'"))
    volume = Variable.Listener(get_volume)
    activewindow = Variable.Listener(hypr)
    Topbar = Widget.EventBox(
        onhover=lambda: print("Hover"),
        onhoverlost=lambda: print("Hover Lost"),
        children=Widget.Box(
            orientation="h",
            valign="center",
            spacing=10,
            children=[
                Widget.Label(date),
                Widget.Label(activewindow, hexpand=True),
                Widget.Label(
                    "volume: 0%",
                    attributes=lambda self: volume.connect(
                        "valuechanged", lambda x: self.set_text(f"volume: {x}%")
                    ),
                ),
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
        size=[0, 50],  # even %
        position="top left right",
        children=Topbar,
    )

    MyFirstWindow.open()
    PotatoLoop()

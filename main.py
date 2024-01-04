#!/usr/bin/python

import json
import os
import subprocess
from datetime import datetime

from PotatoWidgets import PotatoLoop, Style, Variable, Widget

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
        SIGNATURE = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")

        with subprocess.Popen(
            ["socat", "-u", f"UNIX-CONNECT:/tmp/hypr/{SIGNATURE}/.socket2.sock", "-"],
            stdout=subprocess.PIPE,
            text=True,
        ) as proc:
            for line in proc.stdout:
                line = line.replace("\n", "")
                if "activewindow>>" in line:
                    self.set_value(line.split(",")[0].split(">>")[1].capitalize())

    date = Variable.Poll(1000, lambda: subprocess.getoutput("date '+%b %d %I:%M:%S'"))
    volume = Variable.Listener(get_volume)
    activewindow = Variable.Listener(hypr, "")

    Widget.Window(
        props={
            "at": {"top": "20px", "left": "20", "right": 20},  # You can use any
            "size": [0, 50],  # even %
            "position": "top left right",
            "exclusive": True,
        },
        children=Widget.Box(
            orientation="h",
            valign="center",
            spacing=10,
            children=[
                Widget.Button(
                    onclick=lambda: subprocess.run(["notify-send", "Hello", "uwu"]),
                    children=Widget.Label(date),
                ),
                Widget.Label(activewindow, hexpand=True),
                Widget.Box(
                    children=[
                        Widget.Box(
                            orientation="v",
                            children=[
                                Widget.Label(
                                    Variable.Poll(
                                        "1m",
                                        lambda: datetime.now().strftime("%I:%M %p"),
                                    )
                                ),
                                Widget.Label(
                                    Variable.Poll(
                                        "1h",
                                        lambda: datetime.now().strftime("%d/%m/%y"),
                                    )
                                ),
                            ],
                        ),
                        Widget.Box(
                            spacing=5,
                            children=[
                                Widget.Icon("audio-volume-medium-symbolic"),
                                Widget.Icon(
                                    "network-wireless-signal-excellent-symbolic"
                                ),
                                Widget.Icon("battery-full-charged-symbolic"),
                                Widget.Label(
                                    "volume: 0%",
                                    attributes=lambda self: volume.connect(
                                        "valuechanged",
                                        lambda x: self.set_text(f"volume: {x}%"),
                                    ),
                                ),
                            ],
                        ),
                    ]
                ),
            ],
        ),
    ).open()

    Style("./style.css")
    PotatoLoop()

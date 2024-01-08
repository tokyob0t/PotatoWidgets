#!/usr/bin/python

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
                    self.set_value(line.split(",")[1].title())

    def gen_workspace(index):
        return Widget.Button(
            onclick=lambda: subprocess.run(["notify-send", "test", f"{index}"]),
            children=Widget.Label(index),
        )

    date = Variable.Poll(1000, lambda: subprocess.getoutput("date '+%b %d %I:%M:%S'"))
    volume = Variable.Listener(get_volume)
    activewindow = Variable.Listener(hypr)

    Widget.Window(
        props={
            "at": {"top": "20px", "left": "20", "right": 20},  # You can use any
            "size": [0, 50],  # even %
            "position": "top left right",
            "exclusive": True,
        },
        children=Widget.Box(
            [
                Widget.EventBox(
                    classname="eventboxtest",
                    children=Widget.Box(
                        valign="center",
                        spacing=10,
                        children=[
                            (
                                lambda index: Widget.Button(
                                    valign="center",
                                    onclick=lambda: subprocess.run(
                                        [
                                            "hyprctl",
                                            "dispatch",
                                            "workspace",
                                            f"{index}",
                                        ],
                                        stdout=subprocess.PIPE,
                                    ),
                                    children=Widget.Label(
                                        str(index),
                                        valign="center",
                                    ),
                                )
                            )(i)
                            for i in range(1, 10)
                        ],
                    ),
                ),
                Widget.Label(
                    activewindow, hexpand=True, halign="center", valign="center"
                ),
                Widget.Box(
                    spacing=10,
                    children=[
                        Widget.Box(
                            orientation="v",
                            valign="center",
                            children=[
                                Widget.Label(
                                    Variable.Poll(
                                        "1s",
                                        lambda: datetime.now().strftime("%I:%M:%S %p"),
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
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ).open()
    Style("./style.scss")
    PotatoLoop()

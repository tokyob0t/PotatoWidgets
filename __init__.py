#!/usr/bin/python


import subprocess
from datetime import datetime

import src.Variable as Variable
import src.Widget as Widget
from src.__Import import *

if __name__ == "__main__":
    time = Variable.Poll(interval=1000, callback=lambda: subprocess.getoutput("date"))
    # # or
    # time = Variable.Poll(interval=1000, callback=lambda: datetime.now())

    MyFirstWindow = Widget.Window(
        props={
            "at": {"top": "20px", "left": "20", "right": 20},  # You can use any
            "size": [0, "5%"],  # even %
            "position": "left top right",
        },
        children=Widget.Box(
            classname="TESTBOX",
            children=[
                Widget.Label("Start"),
                Widget.Box(
                    hexpand=True,
                    halign="center",
                    children=[
                        Widget.Button(
                            Widget.Label("Botón"),
                            onclick=lambda: subprocess.run(["notify-send", "A", "B"]),
                            valign="center",
                        )
                    ],
                ),
                Widget.Box(
                    orientation="v",
                    # Vertical align
                    valign="center",
                    children=[Widget.Label("Top"), Widget.Label("Bottom")],
                ),
            ],
        ),
    )

    MyFirstWindow.open()
    Gtk.main()

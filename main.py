#!/usr/bin/python


import json
import os
import subprocess
from datetime import datetime

from PotatoWidgets import PotatoLoop, Variable, Widget

if __name__ == "__main__":
    test2 = Variable.Poll(1000, lambda: subprocess.getoutput("date"))

    MyFirstWindow = Widget.Window(
        props={
            "at": {"top": "20px", "left": "20", "right": 20},  # You can use any
            "size": [450, 500],  # even %
            "position": "center",
        },
        children=Widget.Box(
            orientation="v",
            children=[Widget.Label(test2)],
        ),
    )

    MyFirstWindow.open()
    PotatoLoop()

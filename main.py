#!/usr/bin/python


import json
import subprocess
from datetime import datetime

from PotatoWidgets import PotatoLoop, Variable, Widget

if __name__ == "__main__":
    MyFirstWindow = Widget.Window(
        props={
            "at": {"top": "20px", "left": "20", "right": 20},  # You can use any
            "size": [450, 500],  # even %
            "position": "center",
        },
        children=Widget.Scroll(
            orientation="v",
            children=Widget.Box(
                orientation="v",
            ),
        ),
    )

    MyFirstWindow.open()
    PotatoLoop()

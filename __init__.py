#!/usr/bin/python


import json
import subprocess
from datetime import datetime

import src.Variable as Variable
import src.Widget as Widget
from src.__Import import *

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
    Gtk.main()

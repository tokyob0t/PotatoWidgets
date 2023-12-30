#!/usr/bin/python

import subprocess

import src.Variable as Variable
import src.Widget as Widget
from src.__Import import *

if __name__ == "__main__":
    time = Variable.Poll(interval=1000, callback=lambda: subprocess.getoutput("date"))

    MyFirstWindow = Widget.Window(
        props={
            "at": {"top": 20, "left": 20, "right": 20},
            "size": [0, "5%"],
            "position": "left top right",
            "exclusive": True,
        },
        children=Widget.Box(
            classname="TESTBOX",
            children=[
                Widget.Label("Start"),
                Widget.Label(time, bind=time, halign="center", hexpand=True),
                Widget.Box(
                    orientation="v",
                    valign="center",
                    children=[Widget.Label("Top"), Widget.Label("Bottom")],
                ),
            ],
        ),
    )

    MyFirstWindow.open()
    Gtk.main()

## PotatoWidgets  

#### Wiki Under construction  

#### PotatoWidgets is a Python library or framework designed to simplify interaction with Python and GTK. It focuses on being simple yet powerful, drawing inspiration from AGS and EWW. The syntax is designed to be declarative, providing an intuitive way to define GTK widgets  

### Syntax

```py
#!/usr/bin/python

import subprocess

from datetime import datetime

from PotatoWidgets import PotatoLoop, Variable, Widget



if __name__ == "__main__":

    time = Variable.Poll(interval=1000, callback=lambda: subprocess.getoutput("date"))
    # # or 
    # time = Variable.Poll(interval=1000, callback=lambda: datetime.now())

    MyFirstWindow = Widget.Window(
        props={
            "at": {
                "top": "20px",
                "left": "20",
                "right": 20},       # You can use any
            "size": [0, "5%"],      # even %
            "position": "left top right",
        },
        children=Widget.Box(
            classname="TESTBOX",
            children=[
                Widget.Label("Start"),
                Widget.Label(
                    time,
                    # Horizontal align
                    halign="center",
                    # Horizontal expand
                    hexpand=True),
                Widget.Box(
                    orientation="v",
                    # Vertical align
                    valign="center",
                    children=[
                        Widget.Label("Top"),
                        Widget.Label("Bottom")
                    ]
                ),
            ],
        ),
    )

    MyFirstWindow.open()
    PotatoLoop()

```

![img](./img/Preview.png)  
  
#### Installation

```bash
pip install git+https://github.com/T0kyoB0y/PotatoWidgets.git

```

##### ToDo

* Add Dynamic variables
  * [X] Poll      - Timeout + Callback
  * [X] Variable - GObject Variable that notifies when it's value changes
  * [ ] Listener  - Callback then await for changes

* Add more widgets
  * [X] Label
  * [X] Button
  * [X] ToggleButton
  * [X] Box
  * [X] SwitchButton
  * [X] CheckBox
  * [ ] EventBox
  * [ ] CenterBox
  * [ ] ComboBox
  * [X] Image
  * [ ] Icon
  * [X] Scroll
  * [ ] Potato
  * [ ] Stack

* [X] Use GObject to detect dynamic variables in Widgets Props to update Widgets
* [ ] Add a CLI utility(?
* [ ] Help x.x

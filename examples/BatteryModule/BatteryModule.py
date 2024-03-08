from PotatoWidgets import BatteryService, Widget

BatteryModule = Widget.Overlay(
    [
        Widget.ProgressBar(
            value=BatteryService().bind("percentage"),
            orientation="v",
            halign="center",
            classname="battery-progress",
            inverted=True,
        ),
        # Nerd Font as icon
        Widget.Label(text="󱐋", css="color: #111;", classname="nf-icon"),
    ]
)

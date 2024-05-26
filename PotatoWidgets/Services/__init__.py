"""
This module includes various classes related to application management, battery services,
notification handling, service management, and styling.

    App: Class for managing applications.
    Applications: Module for managing multiple applications.
    BatteryService: Class for managing battery-related services.
    HyprlandService: Class for managing Hyprland services.
    Notification: Class for handling notifications.
    NotificationsDbusService: Class for managing notifications via D-Bus.
    NotificationsService: Class for managing notification services.
    Service: Base class for managing services.
    ServiceChildren: Class for managing child services.
    Style: Module for styling applications and widgets.
"""

__all__ = [
    "Applications",
    "BatteryService",
    "NotificationsService",
    #    "TrayService",
]
from .Applications import App, Applications
from .Battery import BatteryService
from .Notifications import Notification, NotificationsService
from .Service import Service
from .Style import Style

# from .Tray import TrayItem, TrayService

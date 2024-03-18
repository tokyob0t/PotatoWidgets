from modules import *

from PotatoWidgets import GLib, PotatoLoop
from PotatoWidgets.Services import (Applications, BatteryService,
                                    HyprlandService, NotificationsDbusService,
                                    NotificationsService)


def main() -> None:
    def SpawnServices() -> None:

    # PotatoLoop()

    MyTopbar.open()
    GLib.MainLoop().run()


if __name__ == "__main__":
    main()

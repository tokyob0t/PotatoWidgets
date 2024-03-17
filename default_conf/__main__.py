from modules import *

from PotatoWidgets import GLib, PotatoLoop


def main() -> None:
    # PotatoLoop()

    MyTopbar.open()
    GLib.MainLoop().run()


if __name__ == "__main__":
    main()

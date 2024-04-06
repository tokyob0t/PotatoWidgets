from modules import *

from PotatoWidgets import PotatoLoop


def main() -> None:

    MyTopbar.open()
    PotatoLoop(run_without_services=True)


if __name__ == "__main__":
    main()

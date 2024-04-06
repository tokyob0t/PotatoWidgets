from ._Logger import Logger
from .Cli import PotatoDbusService
from .Env import *
from .Imports import *
from .Services import (Applications, NotificationsDbusService,
                       NotificationsService, Style)

__all__ = ["PotatoLoop"]


def PotatoLoop(
    confdir: str = DIR_CONFIG_POTATO, *, run_without_services: bool = False
) -> NoReturn:
    """Starts the Potato application loop and initializes necessary services.

    Args:
        confdir (str, optional): The directory path for configuration. Defaults to DIR_CONFIG_POTATO.
        run_without_services (bool, optional): If True, the loop will start without initializing services. Defaults to False.

    Returns:
        NoReturn: This function does not return anything.

    Raises:
        KeyboardInterrupt: If the loop is interrupted by a keyboard event.
        Exception: If any other exception occurs during the loop execution.
    """

    if confdir.endswith("/"):
        confdir = confdir[:-1]

    GLibLoop: GLib.MainLoop = GLib.MainLoop()
    ServicesThread: Union[GLib.Thread, None] = None

    def SpawnServices() -> None:
        """Initialize necessary services for Potato application."""
        # Init classes
        Style.load_css(f"{confdir}/style.scss")
        Applications()
        NotificationsService()
        NotificationsDbusService()
        PotatoDbusService(confdir)

    try:
        # Then run the MainLoop
        if not run_without_services:
            ServicesThread = GLib.Thread.new(SpawnServices.__name__, SpawnServices)
        GLibLoop.run()
    except KeyboardInterrupt:
        Logger.SUCCESS("\n\nBye :)")
        GLibLoop.quit()

    except Exception as r:
        Logger.ERROR(r)
        GLibLoop.quit()

    finally:
        if ServicesThread is not None:
            ServicesThread.unref()

        exit(0)

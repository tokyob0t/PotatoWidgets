from ._Logger import Logger
from .Cli import PotatoService
from .Env import *
from .Imports import *
from .Services.Style import Style

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

    def SpawnServices() -> None:
        """Initialize necessary services for Potato application."""
        Style.load_css(f"{confdir}/style.scss")
        PotatoService(confdir)

    try:
        # Then run the MainLoop
        if not run_without_services:
            SpawnServices()
        GLibLoop.run()
    except KeyboardInterrupt:
        Logger.SUCCESS("\n\nBye :)")
        GLibLoop.quit()

    except Exception as r:
        Logger.ERROR(r)
        GLibLoop.quit()

    finally:
        exit(0)

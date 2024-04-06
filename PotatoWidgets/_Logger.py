class Logger:
    class Colors:
        RESET = "\033[0m"
        BOLD = "\033[1m"

        # Warning Scale
        ERROR = "\033[1;91m"  # Bold red for critical errors
        WARNING = "\033[1;33m"  # Bold yellow for important warnings
        DEPRECATED = "\033[1;35m"  # Bold magenta for deprecated messages
        DEBUG = "\033[1;94m"  # Bold light blue for debugging messages
        SUCCESS = "\033[1;92m"  # Bold green for indicating success

    @staticmethod
    def _log(color_code, *args, **kwargs):
        print(color_code, *args, **kwargs)
        print(Logger.Colors.RESET, end="")

    @staticmethod
    def DEPRECATED(*args, **kwargs):
        Logger._log(Logger.Colors.DEPRECATED, "DEPRECATED:", *args, **kwargs)

    @staticmethod
    def WARNING(*args, **kwargs):
        Logger._log(Logger.Colors.WARNING, "WARNING:", *args, **kwargs)

    @staticmethod
    def SUCCESS(*args, **kwargs):
        Logger._log(Logger.Colors.SUCCESS, "SUCCESS:", *args, **kwargs)

    @staticmethod
    def DEBUG(*args, **kwargs):
        Logger._log(Logger.Colors.DEBUG, "DEBUG:", *args, **kwargs)

    @staticmethod
    def ERROR(*args, **kwargs):
        Logger._log(Logger.Colors.ERROR, "ERROR:", *args, **kwargs)

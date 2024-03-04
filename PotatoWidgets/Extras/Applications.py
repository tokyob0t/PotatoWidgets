from ..Env import *
from ..Imports import *


class App(dict):
    """
    Represents a desktop application.
    """

    def __init__(self, app: Gio.DesktopAppInfo) -> None:
        """
        Initializes an instance of App.

        Args:
            app (Gio.DesktopAppInfo): The desktop application information.
        """
        super().__init__()

        self._app: Gio.DesktopAppInfo = app
        self._keywords: str = " ".join(
            [
                re_sub(r"[^a-zA-Z0-9 ]", "", i.lower())
                for i in [
                    self.name,
                    self.comment,
                    self.categories,
                    self.generic_name,
                    self.display_name,
                ]
            ]
        )
        self["icon_name"] = self.icon_name
        self["name"] = self.name
        self["comment"] = self.comment
        self["desktop"] = self.desktop
        self["categories"] = self.categories
        self["keywords"] = self.keywords

    @property
    def app(self) -> Gio.DesktopAppInfo:
        """Gets the desktop application information."""
        return self._app

    @property
    def name(self) -> str:
        """Gets the name of the application."""
        return self._app.get_name() or ""

    @property
    def generic_name(self) -> str:
        """Gets the generic name of the application."""
        return self._app.get_generic_name() or ""

    @property
    def display_name(self) -> str:
        """Gets the display name of the application."""
        return self._app.get_display_name() or ""

    @property
    def comment(self) -> str:
        """Gets the comment of the application."""
        return self._app.get_description() or ""

    @property
    def categories(self) -> str:
        """Gets the categories of the application."""
        _cat = self._app.get_categories()
        return " ".join(_cat.split(";")) if _cat else ""

    @property
    def desktop(self) -> str:
        """Gets the desktop identifier of the application."""
        return self._app.get_id() or ""

    @property
    def icon_name(self) -> str:
        """Gets the icon name of the application."""
        return self._app.get_string("Icon") or ""

    @property
    def keywords(self) -> str:
        """Gets the keywords of the application."""
        return self._keywords or ""

    def json(self) -> dict:
        """Returns a JSON representation of the application."""
        return dict(super().items())

    def launch(self) -> bool:
        """Launches the application."""
        return self._app.launch()


class Applications:
    """
    Represents a collection of desktop applications.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initializes an instance of Applications."""
        self._json = self._load_json()
        self._preferred = self._json["preferred"]
        self._blacklist = self._json["blacklist"]
        self._all = [
            App(i)
            for i in Gio.DesktopAppInfo.get_all()
            if i.should_show()
            and not any(i.get_name().lower() in j.lower() for j in self._blacklist)
        ]

    @property
    def all(self) -> list[App]:
        """Gets all the applications."""
        return self._all

    def add_preferred(self, name: str) -> None:
        """
        Adds an application to the preferred list.

        Args:
            name (str): The name of the application to add.
        """
        self._json["preferred"].append(name)
        self.reload()

    def get_preferred(self) -> list:
        """Gets the preferred applications list."""
        return self._json["preferred"]

    def add_blacklist(self, name: str) -> None:
        """
        Adds an application to the blacklist.

        Args:
            name (str): The name of the application to add.
        """
        self._json["blacklist"].append(name)
        self.reload()

    def get_blacklist(self) -> list:
        """Gets the blacklist of applications."""
        return self._json["preferred"]

    def query(self, keywords: str) -> Union[List[App], List[None]]:
        """
        Queries applications based on keywords.

        Args:
            keywords (str): The keywords to search for.

        Returns:
            Union[List[App], List[None]]: List of matching applications.
        """
        _matches = [i for i in self.all if keywords in i.keywords]
        if _matches:
            _matches.sort(key=lambda _app: _app.name)
            return _matches
        else:
            return []

    def _load_json(self) -> dict:
        """
        Loads JSON data from a file.

        Returns:
            dict: Loaded JSON data.
        """
        try:
            with open(FILE_APPS_CACHE, "r") as file:
                return json.load(file)
        except json.decoder.JSONDecodeError:
            return {"preferred": [], "blacklist": []}

    def _save_json(self) -> None:
        """Saves JSON data to a file."""
        data = {
            "preferred": self._json["preferred"],
            "blacklist": self._json["blacklist"],
        }
        with open(FILE_APPS_CACHE, "w") as file:
            json.dump(data, file, indent=1)

    def reload(self) -> None:
        """Reloads the JSON data."""
        self._save_json()
        self._json = self._load_json()
        self._preferred = self._json["preferred"]
        self._blacklist = self._json["blacklist"]

    def __str__(self) -> str:
        """Returns a string representation of the JSON data."""
        return str(self._json)

    def __repr__(self) -> str:
        """Returns a string representation of the JSON data."""
        return self.__str__()

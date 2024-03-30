"""
This file includes the following classes:

- App: Represents a desktop application.
- Applications: Represents a collection of desktop applications.

Class App Methods:
- app: Gets the desktop application information.
- name: Gets the name of the application.
- generic_name: Gets the generic name of the application.
- display_name: Gets the display name of the application.
- comment: Gets the comment of the application.
- categories: Gets the categories of the application.
- desktop: Gets the desktop identifier of the application.
- icon_name: Gets the icon name of the application.
- keywords: Gets the keywords of the application.
- json: Returns a JSON representation of the application.
- launch: Launches the application.

Class Applications Methods:
- get_all: Gets all the applications.
- add_preferred: Adds an application to the preferred list.
- get_preferred: Gets the preferred applications list.
- add_blacklist: Adds an application to the blacklist.
- get_blacklist: Gets the blacklist of applications.
- add_whitelist: Adds an application to the whitelist.
- get_whitelist: Gets the whitelist of applications.
- query: Queries applications based on keywords.
- json: Returns a JSON representation of the applications.
- reload: Reloads the JSON data.
"""

from ..Env import *
from ..Imports import *
from .Service import Service


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
        # self._context = Gio.AppLaunchContext().new()

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
        # return self._app.launch()

        _proc: Gio.Subprocess = Gio.Subprocess.new(
            flags=Gio.SubprocessFlags.STDERR_SILENCE
            | Gio.SubprocessFlags.STDOUT_SILENCE,
            argv=["gtk-launch", self.desktop],
        )
        return _proc.wait_check()


class Applications(Service):
    """
    Represents a collection of desktop applications.

    Methods:
    - get_all: Get all applications.
    - add_preferred: Add an application to the preferred list.
    - get_preferred: Get the preferred applications list.
    - add_blacklist: Add an application to the blacklist.
    - get_blacklist: Get the blacklist of applications.
    - add_whitelist: Add an application to the whitelist.
    - get_whitelist: Get the whitelist of applications.
    - query: Query applications based on keywords.
    - json: Get JSON representation of the applications.
    - reload: Reload the JSON data.
    """

    def __init__(self) -> None:
        """Initializes an instance of Applications."""

        self._json: Dict[str, List[Union[str, None]]] = self._load_json()
        self._preferred: List[Union[str, None]] = self._json.get("preferred", [])
        self._blacklist: List[Union[str, None]] = self._json.get("blacklist", [])
        self._whitelist: List[Union[str, None]] = self._json.get("whitelist", [])

        self._all = [
            App(i)
            for i in Gio.DesktopAppInfo.get_all()
            if (
                i.should_show()
                and not any(
                    j.lower() in i.get_name().lower() for j in self.get_blacklist() if j
                )
            )
            or any(j.lower() in i.get_name().lower() for j in self.get_whitelist() if j)
        ]

        self._all.sort(key=lambda app: app.name)

    def get_all(self) -> Union[List[App], List[None]]:
        """Gets all the applications."""
        return self._all

    def add_preferred(self, name: str) -> None:
        """
        Adds an application to the preferred list.

        Args:
            name (str): The name of the application to add.
        """
        if name not in self._preferred:
            self._preferred.append(name)
            self.reload()

    def get_preferred(self) -> List[Union[None, str]]:
        """Gets the preferred applications list."""
        return self._preferred

    def add_blacklist(self, name: str) -> None:
        """
        Adds an application to the blacklist.

        Args:
            name (str): The name of the application to add.
        """
        if name not in self._blacklist:
            self._blacklist.append(name)
            self.reload()

    def get_blacklist(self) -> List[Union[str, None]]:
        """Gets the blacklist of applications."""
        return self._blacklist

    def add_whitelist(self, name: str) -> None:
        """
        Adds an application to the whitelist.

        Args:
            name (str): The name of the application to add.
        """
        if name not in self._whitelist:
            self._whitelist.append(name)
            self.reload()

    def get_whitelist(self) -> List[Union[None, str]]:
        """Gets the whitelist of applications."""
        return self._whitelist

    def query(self, keywords: str) -> List[Union[App, None]]:
        """
        Queries applications based on keywords.

        Args:
            keywords (str): The keywords to search for.

        Returns:
            Union[List[App], List[None]]: List of matching applications.
        """
        keywords = keywords.lower()
        return [i for i in self.get_all() if i and keywords in i.keywords]

    def _load_json(self) -> Dict[str, List[Union[str, None]]]:
        """
        Loads JSON data from a file.

        Returns:
            dict: Loaded JSON data.
        """
        try:
            with open(FILE_CACHE_APPS, "r") as file:
                return json.load(file)

        except json.decoder.JSONDecodeError:
            return {"preferred": [], "blacklist": [], "whitelist": []}

    def _save_json(self) -> None:
        """Saves JSON data to a file."""
        data = {
            "preferred": self._preferred,
            "blacklist": self._blacklist,
            "whitelist": self._whitelist,
        }
        with open(FILE_CACHE_APPS, "w") as file:
            json.dump(data, file, indent=1)

    def reload(self) -> None:
        """Reloads the JSON data."""
        self._save_json()
        self._json: Dict[str, List[Union[str, None]]] = self._load_json()
        self._preferred: List[Union[str, None]] = self._json["preferred"]
        self._blacklist: List[Union[str, None]] = self._json["blacklist"]
        self._whitelist: List[Union[str, None]] = self._json["whitelist"]

    def json(self) -> dict:
        """Returns a JSON representation of the applications."""
        return self._json

    def __str__(self) -> str:
        """Returns a string representation of the JSON data."""
        return str(self.json())

    def __repr__(self) -> str:
        """Returns a string representation of the JSON data."""
        return self.__str__()

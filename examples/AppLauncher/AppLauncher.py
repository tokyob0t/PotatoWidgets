from PotatoWidgets import Variable, Widget, lookup_icon
from PotatoWidgets.Services import Applications


def GenerateApp(entry):
    _actioned = lambda: (
        entry.launch(),
        AppLauncher.close(),
        AppQuery.set_value(""),
        AppEntry.set_text(""),
    )

    _app = Widget.Revealer(
        valign="start",
        transition="slideup",
        duration=250,
        reveal=True,
        attributes=lambda self: (
            setattr(self, "keywords", entry.keywords),
            setattr(self, "launch", _actioned),
            self.bind(
                AppQuery,
                lambda query: self.set_revealed(str(query).lower() in self.keywords),
            ),
        ),
        children=Widget.Button(
            classname="app",
            valign="start",
            onclick=_actioned,
            children=Widget.Box(
                spacing=10,
                children=[
                    Widget.Image(lookup_icon(entry.icon_name), 35),
                    Widget.Box(
                        orientation="v",
                        vexpand=True,
                        children=[
                            Widget.Label(
                                entry.name.title(),
                                wrap=True,
                                halign="start",
                                valign=("center" if not entry.comment else "start"),
                                vexpand=(True if not entry.comment else False),
                                classname="name",
                            ),
                            Widget.Label(
                                entry.comment or entry.generic_name,
                                wrap=True,
                                visible=bool(entry.comment or entry.generic_name),
                                classname="comment",
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )
    return _app


AppQuery = Variable("")

SortedAppsByName = Applications.get_all()
SortedAppsByName.sort(key=lambda app: app.name)


AppsList = Widget.Scroll(
    hexpand=True,
    vexpand=True,
    children=Widget.Box(
        orientation="v",
        children=[GenerateApp(app) for app in SortedAppsByName],
    ),
)

AppEntry = Widget.Entry(
    onchange=AppQuery.set_value,
    onenter=lambda text: next(
        app.launch()
        for app in AppsList.get_children()[0].get_children()[0].get_children()
        if str(text).lower() in app.keywords
    ),
)


AppLauncher = Widget.Window(
    size=[500, 600],
    layer="dialog",
    namespace="AppLauncher",
    children=Widget.Box(
        classname="launcher",
        orientation="v",
        spacing=20,
        children=[
            AppEntry,
            AppsList,
        ],
    ),
)

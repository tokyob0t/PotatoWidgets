from PotatoWidgets import Applications, Variable, Widget, lookup_icon


def GenerateApp(entry):
    _app = Widget.Revealer(
        valign="start",
        transition="slideup",
        duration=250,
        reveal=True,
        attributes=lambda self: (
            setattr(self, "app", entry),
            setattr(self, "keywords", entry.keywords),
            self.bind(
                AppQuery, lambda query: self.set_revealed(query in self.keywords)
            ),
        ),
        children=Widget.Button(
            classname="app",
            valign="start",
            onclick=lambda: (
                entry.launch(),
                AppLauncher.close(),
                AppQuery.set_value(""),
            ),
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
                                classname="name",
                            ),
                            Widget.Label(
                                entry.comment or entry.generic_name,
                                wrap=True,
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
AppsList = Widget.Scroll(
    hexpand=True,
    vexpand=True,
    children=Widget.Box(
        orientation="v",
        children=[GenerateApp(app) for app in Applications().all()],
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
            Widget.Entry(
                onchange=AppQuery.set_value,
                onenter=lambda text: next(
                    app_revealer.app.launch()
                    for app_revealer in AppsList.get_children()[0]
                    .get_children()[0]
                    .get_children()
                    if text in app_revealer.keywords
                ),
            ),
            AppsList,
        ],
    ),
)

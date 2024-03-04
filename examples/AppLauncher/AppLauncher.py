from PotatoWidgets import Gio, Gtk, PotatoLoop, Variable, Widget, lookup_icon
from PotatoWidgets.Extras import Applications


def GenerateApp(entry):
    _app = Widget.Revealer(
        css="padding-bottom: 13px;",
        valign="start",
        transition="slideup",
        duration=250,
        reveal=True,
        attributes=lambda self: (
            setattr(self, "app", entry),
            setattr(self, "keywords", entry.keywords),
            self.bind(AppQuery, lambda out: self.set_revealed(out in self.keywords)),
        ),
        children=Widget.Button(
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
                                valign=("center" if not entry.comment else "start"),
                                vexpand=(True if not entry.comment else False),
                                css="color: #fff; font-weight: 700;",
                            ),
                            Widget.Label(
                                entry.comment or entry.generic_name,
                                wrap=True,
                                visible=bool(entry.comment or entry.generic_name),
                                css="color: #aaa; font-weight: normal;",
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

test = next(app for app in Applications().query("a"))

AppLauncher = Widget.Window(
    size=[500, 600],
    # Wayland
    # layer="top",
    #
    # X11
    layer="dialog",
    children=Widget.Box(
        css="background: #111; padding: 40px",
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

AppLauncher.open()


if __name__ == "__main__":
    PotatoLoop()

# from PotatoWidgets import HyprlandService
from PotatoWidgets import Variable, Widget
from PotatoWidgets.Services.Hyprland import HyprlandService

ActiveWorkspace = Variable(0)


# Sorry, I havent fully implemented the Hyprland service yet
HyprlandService.connect(
    "workspacev2", lambda _, id, name: ActiveWorkspace.set_value(id)
)


def WorkspaceButton(id):
    my_button = Widget.Button(
        onclick=lambda: HyprlandService.hyprctl_async(f"dispatch workspace {id}"),
        valign="center",
        children=Widget.Label(id),
    )
    setattr(my_button, "id", id)
    ActiveWorkspace.bind(
        lambda v: (
            my_button.set_css("background: blue")
            if v == getattr(my_button, "id")
            else my_button.set_css("background: unset")
        )
    )

    my_button.set_css("background: unset;")

    return my_button


def Workspaces():
    return list(map(WorkspaceButton, range(1, 11)))

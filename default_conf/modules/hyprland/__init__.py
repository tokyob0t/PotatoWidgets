# from PotatoWidgets import HyprlandService
from PotatoWidgets import Bash, Variable, Widget

Signature = Bash.get_env("HYPRLAND_INSTANCE_SIGNATURE")

ActiveWorkspace = Variable(0)


# Sorry, I havent fully implemented the Hyprland service yet
Bash.popen(
    [
        "bash",
        "-c",
        f"""socat -u UNIX-CONNECT:/tmp/hypr/{Signature}/.socket2.sock - | grep --line-buffered -v -e "socat" -e "destroyworkspace" -e "createworkspace" | grep --line-buffered "workspace>>" """,
    ],
    stdout=lambda stdout: (
        ActiveWorkspace.set_value(
            int(
                stdout.split(">>")[1],
            ),
        ),
    ),
)


def WorkspaceButton(id):
    my_button = Widget.Button(
        onclick=lambda: Bash.run_async(f"hyprctl dispatch workspace {id}"),
        valign="center",
        children=Widget.Label(id),
        attributes=lambda self: (
            setattr(self, "id", id),
            self.bind(
                ActiveWorkspace,
                lambda out: (
                    self.set_css("background: blue;")
                    if out == self.id
                    else self.set_css("background: unset;")
                ),
            ),
        ),
    )
    my_button.set_css("background: unset;")
    return my_button


def Workspaces():
    return list(map(WorkspaceButton, range(1, 11)))
    # return [WorkspaceButton(i) for i in range(1, 11)]

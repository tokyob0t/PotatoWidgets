from typing import Dict, List

from PotatoWidgets import Bash, Variable, Widget

keys: List[str] = Bash.get_output("bspc query --desktops").splitlines()
values: List[int] = [i for i in range(1, len(keys) + 1)]

ActiveWorkspace = Variable(1)
# doing this bc by default bspwm handles workspace names in hex
WorkspaceMapping: Dict[str, int] = {keys[i]: int(values[i]) for i in range(len(keys))}


# bspc subscribe desktop_focus
# desktop_focus <monitor_id> <desktop_id>
# hex id
Bash.popen(
    "bspc subscribe desktop_focus",
    stdout=lambda stdout: ActiveWorkspace.set_value(
        # desktop_focus 0x00200002 0x00200006
        # ["desktop_focus", "0x00200002", "x00200006"]
        # 0                 1             2
        WorkspaceMapping.get(stdout.split()[2], 0)
    ),
)


# Topbar Elements
def WorkspaceButton(id):
    my_button = Widget.Button(
        onclick=lambda: Bash.run(f"bspc desktop --focus {id}"),
        valign="center",
        children=Widget.Label(id),
        attributes=lambda self: (
            setattr(self, "id", id),
            self.bind(
                ActiveWorkspace,
                lambda out: (
                    self.set_css("background: blue;")
                    if out == getattr(self, "id")
                    else self.set_css("background: unset;")
                ),
            ),
        ),
    )
    my_button.set_css("background: unset;")
    return my_button


def Workspaces():
    return [WorkspaceButton(i) for i in WorkspaceMapping.values()]

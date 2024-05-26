from typing import Union

from PotatoWidgets import Playerctl, Variable

# First we create a var to store our players as widgets
PlayersList = Variable([])


# This handles all the players available
# https://lazka.github.io/pgi-docs/Playerctl-2.0/classes/PlayerManager.html
Manager = Playerctl.PlayerManager()

# First add current players
for name in Manager.get_property("player_names") or []:
    Manager.manage_player(
        Playerctl.Player.new_from_name(name),
    )

# Then connect to signals to update players
Manager.connect("name-appeared", lambda *args: UpdatePlayers(*args, new_player=True))
Manager.connect("name-vanished", lambda *args: UpdatePlayers(*args))


# Now make a callback to handle appear/vanish players
def UpdatePlayers(_, player: Playerctl.PlayerName, new_player: bool = False):
    if new_player:
        Manager.manage_player(Playerctl.Player.new_from_name(player))

    # Reload PlayersList var with new players as widgets
    PlayersList.value = list(
        map(
            lambda p: GenerateWidget(*ConnectPlayerToWidgets(p)),
            _manager.props.players,
        )
    )

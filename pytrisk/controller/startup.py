#
# This file is part of pytrisk.
#
# pytrisk is free software: you can redistribute it and/or modify it
# under the # terms of the GNU General Public License as published by
# the Free Software # Foundation, either version 3 of the License, or
# (at your option) any later # version.
#
# pytrisk is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with pytrisk. If not, see <https://www.gnu.org/licenses/>.
#


from pytrisk.config import config
from pytrisk.domain.settings import settings
from pytrisk.events import Events
from pytrisk.logger import log


class StartupController:
    def __init__(self, context, event_bus):
        # Store the app and event bus
        self.context   = context
        self.event_bus = event_bus

    # -- Current state retrieval

    # -- Data retrieval

    def get_available_player_colors(self):
        """Return the list of available player colors."""
        return settings.players.colors

    def get_player_name(self, index):
        """Return the name of a player."""
        return self.context.startup.players[index].name

    def get_default_player_color(self, index):
        """Return the color of a player."""
        key = f"player{index}"
        return config.startup.players[key].color

    def get_maps(self):
        """Return the list of available maps."""
        return self.context.maps.values()

    def get_default_map_name(self):
        """Return the default map."""
        return config.startup.map


    # -- Action handlers

    def set_map_name(self, name: str):
        """Select the map.

        Args:
            name: map name
        """
        log.info(f'Setting map to {name}')
        config.startup.map = name
        self.context.startup.map_name = name


    def set_player_color(self, index, color):
        log.info(f'Setting player {index} color to {color}')
        key = f"player{index}"
        self.context.startup.players[index].color = color
        config.startup.players[key].color         = color
        self.event_bus.emit(Events.player_color_changed, index, color)

    def set_player_name(self, index, name):
        """Set the name of a player.

        Args:
            index: player index
            name: player name
        """
        log.info(f'Setting player {index} name to {name}')
        player = self.context.startup.players[index]

        # Human player is special
        if player.is_human:
            # store new name
            key = f"player{index}"
            config.startup.players[key].name = name
            # if name is empty, use default
            if name == '':
                name = player.default_name
            log.warning(f'Empty name, defaulting to username {name}')

        # Store new name
        player.name = name
        self.event_bus.emit(Events.player_name_changed, index, name)


    # -- Preferences retrieval / setting

    # -- Private methods


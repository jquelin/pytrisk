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


class Controller:
    def __init__(self, context, event_bus):
        # Store the app and event bus
        self.context = context
        self.event_bus = event_bus

    # -- Current state retrieval

    # -- Data retrieval

    def get_available_player_colors(self):
        """Return the list of available player colors."""
        return settings.players.colors

    def get_player_name(self, index):
        """Return the name of a player."""
        return self.context.game.players[index].name

    def get_default_player_color(self, index):
        """Return the color of a player."""
        key = f"player{index}"
        return config.startup.players[key].color

    def get_maps(self):
        """Return the list of available maps."""
        return self.context.maps.values()

    # -- Action handlers

    def do_quit(self):
        """Quit the application."""
        log.info('Request to quit')
        self.event_bus.emit(Events.action_quit)

    def set_player_color(self, index, color):
        log.info(f'Setting player {index} color to {color}')
        key = f"player{index}"
        self.context.game.players[index].color     = color
        config.startup.players[key].color = color
        self.event_bus.emit(Events.player_color_changed, index, color)

    def set_player_name(self, index, name):
        """Set the name of a player.

        Args:
            index: player index
            name: player name
        """
        log.info(f'Setting player {index} name to {name}')
        key = f"player{index}"
        self.context.game.players[index].name = name
        config.startup.players[key].name      = name
        self.event_bus.emit(Events.player_name_changed, index, name)


    # -- Preferences retrieval / setting

    # -- Private methods


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


from pytrisk.domain.colors import PLAYER_COLORS
from pytrisk.events import Events
from pytrisk.logger import log


class Controller:
    def __init__(self, context, event_bus):
        # Store the app and event bus
        self.context = context
        self.event_bus = event_bus

    # -- Current state retrieval

    # -- Data retrieval

    def get_player_colors(self):
        """Return the list of available player colors."""
        return PLAYER_COLORS

    def get_maps(self):
        """Return the list of available maps."""
        return self.context.maps.values()

    # -- Action handlers

    def do_quit(self):
        """Quit the application."""
        log.info('Request to quit')
        self.event_bus.emit(Events.action_quit)


    # -- Preferences retrieval / setting

    # -- Private methods


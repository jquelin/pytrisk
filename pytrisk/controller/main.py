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

from pytrisk.domain.game_context import GameContext
from pytrisk import settings
from pytrisk.events import Events, EventBus
from pytrisk.logger import log


class MainController:
    def __init__(self, controller, context, event_bus):
        # Store the app and event bus
        self.controller              = controller
        self.context   : GameContext = context
        self.event_bus : EventBus    = event_bus


    # -- Current state retrieval

    # -- Data retrieval

    # -- Action handlers

    def do_close_game(self):
        """Close the current game."""
        log.info('Request to close game')
        if not self.context.in_game:
            log.info('No game to close')
            return


    def do_quit(self):
        """Quit the application."""
        log.info('Request to quit')
        self.event_bus.emit(Events.action_quit)


    # -- Preferences retrieval / setting

    def get_gui_wait_time(self) -> int:
        """Get the GUI wait validation time."""
        log.debug('Getting GUI wait validation time')
        return settings.gui.wait_validate

    # -- Private methods


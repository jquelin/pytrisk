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

from dataclasses import dataclass

from pytrisk.config import config
from pytrisk.controller.game     import GameController
from pytrisk.controller.startup  import StartupController
from pytrisk.domain.game_context import GameContext
from pytrisk.domain.settings import settings
from pytrisk.events import Events
from pytrisk.logger import log


@dataclass
class SubControllers:
    startup : StartupController
    game    : GameController

class Controller:
    def __init__(self, context, event_bus):
        # Store the app and event bus
        self.context   : GameContext = context
        self.event_bus : Events      = event_bus

        # subcontrollers
        self.sub = SubControllers(
            startup = StartupController(context, event_bus),
            game    = GameController(context, event_bus)
        )


    # -- Current state retrieval

    # -- Data retrieval

    # -- Action handlers

    def do_close_game(self):
        """Close the current game."""
        log.info('Request to close game')
        if not self.context.in_game:
            log.info('No game to close')
            return
        # self.sub.game.do_close_game()

        self.in_game = False
        # self.game.do_close_game()

    def do_quit(self):
        """Quit the application."""
        log.info('Request to quit')
        self.event_bus.emit(Events.action_quit)


    def do_start_new_game(self):
        """Start a new game."""
        log.info('Delegating to subcontroller to start new game')
        self.sub.game.do_start_new_game()


    # -- Preferences retrieval / setting

    def get_gui_wait_time(self) -> int:
        """Get the GUI wait validation time."""
        log.debug('Getting GUI wait validation time')
        return settings.gui.wait_validate

    # -- Private methods


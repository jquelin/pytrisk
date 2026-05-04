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

from pytrisk.constants       import appinfo
from pytrisk.config          import config
from pytrisk.domain.player   import AIPlayer, HumanPlayer
from pytrisk.domain.settings import settings
from pytrisk.logger          import log


class Game:
    """ Game class, managing a single game. """

    def __init__(self):
        log.info("Creating game")

        # initialize data and game
        self._create_players()


    # -- Private maps

    def _create_players(self):
        '''Create players from previous configuration.
        '''
        log.info('Creating players')
        self.players = []
        self.players.append(HumanPlayer())
        max_count = settings.players.max_count
        log.debug(f'max number of players: {max_count}')
        for i in range(1, max_count):
            self.players.append(AIPlayer(i))

        # disable players to match the configuration
        count = int(config.startup.players.count)
        log.debug(f'current number of players: {count}')
        for i in range(count + 1, max_count):
            self.players[i].enabled = False


    # -- Public methods


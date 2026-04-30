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

from pytrisk.constants  import appinfo
from pytrisk.logger     import log


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



    # -- Public methods


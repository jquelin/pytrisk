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

import getpass

from pytrisk.config        import config
from pytrisk.constants     import appinfo
from pytrisk.domain.colors import PLAYER_COLORS
from pytrisk.logger        import log


class Player:
    def __init__(self, nb: int):
        self.nb = nb
        self.name  = None
        self.color = PLAYER_COLORS[nb]

    @property
    def is_human(self):
        return isinstance(self, HumanPlayer)

    @property
    def is_computer(self):
        return isinstance(self, AIPlayer)


class AIPlayer(Player):
    def __init__(self, nb: int):
        super().__init__(nb)
        config_key = f"ai{nb}"
        self.color = config.startup.player.ai[config_key].color or self.color


class HumanPlayer(Player):
    def __init__(self):
        super().__init__(nb=0)
        self.name  = config.startup.player.human.name or getpass.getuser()
        self.color = config.startup.player.human.color or self.color


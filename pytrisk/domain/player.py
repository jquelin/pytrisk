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

from pytrisk.config          import config
from pytrisk.constants       import appinfo
from pytrisk.domain.settings import settings
from pytrisk.logger          import log


class Player:
    def __init__(self, index: int):
        self.index   = index
        self.name    = None
        self.key     = f'player{index}'
        self.color   = config.get(f"startup.player.{index}.color")
        self.enabled = True

    @property
    def is_human(self):
        return isinstance(self, HumanPlayer)

    @property
    def is_computer(self):
        return isinstance(self, AIPlayer)


class AIPlayer(Player):
    def __init__(self, nb: int):
        super().__init__(nb)


class HumanPlayer(Player):
    def __init__(self):
        super().__init__(index=0)
        self.default_name = getpass.getuser()
        self.name = config.get(f"startup.player.{self.index}.name") or self.default_name


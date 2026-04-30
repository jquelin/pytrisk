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

from pytrisk.config     import config
from pytrisk.constants  import appinfo
from pytrisk.logger     import log


class Player:
    def __init__(self):
        self.name  = None
        self.color = None

    @property
    def is_human(self):
        return isinstance(self, HumanPlayer)

    @property
    def is_computer(self):
        return isinstance(self, AIPlayer)

    colors = [
        '#333333',  # grey20
        '#FF2052',  # awesome
        '#01A368',  # green
        '#0066FF',  # blue
        '#DCB63B',  # ~ dirty yellow
        '#9E5B40',  # sepia
        '#A9B2C3',  # cadet blue
        '#BB3385',  # red violet
        '#FF681F',  # orange
        '#00CCCC',  # robin's egg blue
        '#FFB347',  # pastel orange
        '#2E8B57',  # sea green
        '#4682B4',  # steel blue
        '#C71585',  # medium violet red
        '#708090',  # slate gray
        '#B22222',  # firebrick
        '#DAA520',  # goldenrod
        '#40E0D0',  # turquoise
        '#8A2BE2',  # blue violet
    ]



class AIPlayer(Player):
    def __init__(self, nb: int):
        super().__init__()
        config_key = f"ai{nb}"
        self.color  = config.startup.player.ai[config_key].color or self.colors[nb]


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()
        self.name  = config.startup.player.human.name or getpass.getuser()
        self.color = config.startup.player.human.color or self.colors[0]


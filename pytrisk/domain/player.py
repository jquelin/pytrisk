# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import getpass

from pytrisk.config          import config
from pytrisk.constants       import appinfo
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


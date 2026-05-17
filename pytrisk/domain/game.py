# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

from pytrisk.constants       import appinfo
from pytrisk.config          import config
from pytrisk.logger          import log

from pytrisk.domain.map      import Map
from pytrisk.domain.player   import Player

class Game:
    """ Game class, managing a single game. """

    def __init__(self, map, players):
        """ Constructor.

        Args:
            startup (StartupConfig): Startup configuration.
        """
        log.info("Creating game object")
        self.map     : Map          = map
        self.players : list[Player] = players


    # -- Private maps


    # -- Public methods


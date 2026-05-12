# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

from pytrisk.config        import config
from pytrisk.domain.player import AIPlayer, HumanPlayer
from pytrisk.logger        import log
import pytrisk.settings as settings


class StartupConfig:
    """ Startup configuration, before launching the actual game."""

    def __init__(self):
        log.info("Creating startup config")
        self.map_name = config.get("startup.map")
        self._create_players()


    # -- Private methods

    def _create_players(self):
        '''Create players from previous configuration.'''
        log.info('Creating players')
        self.players = []

        # First player is always human
        self.players.append(HumanPlayer())

        # Then create AI players
        max_count = settings.players.max_count
        log.debug(f'max number of players: {max_count}')
        for i in range(1, max_count):
            self.players.append(AIPlayer(i))

        # Disable AI players to match the configuration
        count = config.get('startup.players.count')
        log.debug(f'current number of players: {count}')
        for i in range(count, max_count):
            self.players[i].enabled = False


    # -- Public methods

    @property
    def nb_players(self):
        """Return the number of enabled players."""
        enabled = [i for i in self.players if i.enabled]
        return len(enabled)


    def get_final_players(self) -> list:
        """Return the list of players ready for the game.

        Returns:
            list: List of enabled players
        """
        log.info(f'final number of players: {self.nb_players}')
        return [p for p in self.players if p.enabled]

# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

from pytrisk.constants       import appinfo
from pytrisk.config          import config
from pytrisk.logger          import log

from pytrisk.domain.ai       import AINames
from pytrisk.domain.map      import Map
from pytrisk.domain.player   import Player
from pytrisk.events          import Events

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

        self._assign_ai_names()


    # -- Private methods

    def _assign_ai_names(self):
        """Assign names to AI players."""
        ainames = AINames()
        for player in self.players:
            if player.is_computer:
                newname = ainames.get_name()
                player.name = newname
                log.debug(f'Assigning AI name: {player.index} is now called {newname}')


    # -- Public methods

    def distribute_initial_territories(self):
        """ Distribute initial territories among players, one by one."""

        nb_players = len(self.players)
        nb_countries = len(self.map.countries)
        log.info(f"Distributing {nb_countries} initial territories to {nb_players} players")
        events = []

        for country in self.map.countries:
            owner = self.players[country.id % nb_players]
            log.debug(f"Assigning country {country.id} to player {owner}")
            country.set_owner(owner)
            country.armies = 1
            events.append((Events.country_chown, country, None, owner))

        return events

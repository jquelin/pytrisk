# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import time

from pytrisk.constants      import appinfo
from pytrisk.domain.game    import Game
from pytrisk.domain.map     import Map
from pytrisk.domain.startup import StartupConfig
from pytrisk.logger         import log


class GameContext:
    """ GameContext class, main entry point for the controller. """

    def __init__(self):
        # Load maps
        self._create_maps()

        # Create a startup configuration
        self.startup = StartupConfig()
        self.game    = None

        # other stuff that may come later on
        #self.settings = Settings()
        #self.available_ai = AIRegistry()
        #self.statistics = Statistics()


    # -- Public properties

    @property
    def in_game(self):
        return self.game is not None


    # -- Private maps

    def _create_maps(self):
        '''Create maps from map definition. It is not yet fully loaded.
        '''
        log.info('Creating maps')
        start = time.perf_counter()
        mapdir = appinfo.dirs.share / 'maps'
        self.maps = {}
        for f in mapdir.iterdir():
            if f.is_dir():
                self.maps[f.name] = Map(f)

        end = time.perf_counter()
        log.info(f'Created {len(self.maps)} maps in {end - start:.2f} seconds')


    # -- Public methods

    def new_game(self):
        """Start a new game."""
        log.info("Creating new game")
        map     = self.maps[self.startup.map_name]
        players = self.startup.get_final_players()
        self.game : Game = Game(map, players)


    def end_game(self):
        log.info("Ending game")
        # self.game = None

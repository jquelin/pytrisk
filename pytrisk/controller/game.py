# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.


from pytrisk.config import config
from pytrisk.domain.continent import Continent
from pytrisk.domain.game_context import GameContext
from pytrisk.domain.player import Player
from pytrisk.events import EventBus, Events
from pytrisk.logger import log


class GameController:
    def __init__(self, controller, context, event_bus):
        # Store the app and event bus
        self.controller              = controller
        self.context   : GameContext = context
        self.event_bus : EventBus    = event_bus

    # -- Current state retrieval

    # -- Data retrieval

    def get_continents(self) -> list[Continent]:
        """Return the list of continents."""
        return self.context.game.map.continents


    def get_map_image_files(self):
        """Return the map image files.

        Returns:
            tuple: (background, overlay)
        """
        return self.context.game.map.background, self.context.game.map.overlay


    def get_players(self) -> list[Player]:
        """Return the list of players."""
        return self.context.game.players

    # -- Action handlers

    def do_start_new_game(self):
        """Start a new game."""
        log.info('Actually starting a new game')

        # First create a new game
        self.context.new_game()
        self.context.game.map.load()
        # TODO: randomize player order

        # Once the game is initialized, signal the GUI
        self.event_bus.emit(Events.new_game)

        # Now, distribute the initial territories
        events = self.context.game.distribute_initial_territories()
        for e in events:
            self.event_bus.emit(*e)

        # TODO: check if distribution is equal




    # -- Preferences retrieval / setting

    def set_aspect_ratio(self, ratio: bool):
        """Set the aspect ratio of the map.

        Args:
            ratio: whether to keep the aspect ratio
        """
        log.info(f'Setting aspect ratio to {ratio}')
        config.set('gui.aspect.keep_ratio', ratio)
        self.event_bus.emit(Events.aspect_ratio_changed)


    # -- Private methods


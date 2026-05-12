# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

from pytrisk.config import config
from pytrisk.domain.game_context import GameContext
from pytrisk.events import EventBus, Events
from pytrisk.logger import log
import pytrisk.settings as settings


class StartupController:
    def __init__(self, controller, context, event_bus):
        # Store the app and event bus
        self.controller              = controller
        self.context   : GameContext = context
        self.event_bus : EventBus    = event_bus


    # -- Current state retrieval

    # -- Data retrieval

    def get_available_player_colors(self):
        """Return the list of available player colors."""
        return settings.players.colors

    def get_player_name(self, index):
        """Return the name of a player."""
        return self.context.startup.players[index].name

    def get_max_players(self):
        """Return the maximum number of players."""
        return settings.players.max_count

    def get_nb_players(self):
        """Return the number of players."""
        return self.context.startup.nb_players

    def get_maps(self):
        """Return the list of available maps."""
        return self.context.maps.values()

    def get_default_map_name(self):
        """Return the default map."""
        return config.get("startup.map")


    # -- Action handlers

    def set_map_name(self, name: str):
        """Select the map.

        Args:
            name: map name
        """
        log.info(f'Setting map to {name}')
        config.set("startup.map", name)
        self.context.startup.map_name = name

    def set_nb_players(self, nb_players):
        log.info(f'Setting number of players to {nb_players}')
        curnb = self.context.startup.nb_players
        newnb = nb_players

        # First check if it's a valid number
        try:
            nb_players = int(nb_players)
        except Exception:
            log.warning(f'Not a valid number, reverting to {curnb}')
            newnb = curnb


        # Then validate if it's within bounds
        if nb_players < 2:
            log.warning('Too few players, setting to 2')
            newnb = 2

        max_players = self.get_max_players()
        if nb_players > max_players:
            log.warning(f'Too many players, setting to max players ({max_players})')
            newnb = max_players

        # Store new number & inform the view
        config.set("startup.players.count", newnb)
        self.event_bus.emit(Events.nb_players_changed, newnb)


    def set_player_color(self, index, color):
        log.info(f'Setting player {index} color to {color}')
        self.context.startup.players[index].color = color
        config.set(f"startup.player.{index}.color", color)
        self.event_bus.emit(Events.player_color_changed, index, color)

    def set_player_name(self, index, name):
        """Set the name of a player.

        Args:
            index: player index
            name: player name
        """
        log.info(f'Setting player {index} name to {name}')
        player = self.context.startup.players[index]

        # Human player is special
        if player.is_human:
            # store new name
            key = f"player{index}"
            config.set(f"startup.player.{key}.name", name)
            # if name is empty, use default
            if name == '':
                name = player.default_name
            log.warning(f'Empty name, defaulting to username {name}')

        # Store new name
        player.name = name
        self.event_bus.emit(Events.player_name_changed, index, name)


    # -- Preferences retrieval / setting

    # -- Private methods


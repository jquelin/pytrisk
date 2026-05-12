# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

from pytrisk.domain.game_context import GameContext
from pytrisk.events import Events, EventBus
from pytrisk.logger import log
import pytrisk.settings as settings


class MainController:
    def __init__(self, controller, context, event_bus):
        # Store the app and event bus
        self.controller              = controller
        self.context   : GameContext = context
        self.event_bus : EventBus    = event_bus


    # -- Current state retrieval

    # -- Data retrieval

    # -- Action handlers

    def do_close_game(self):
        """Close the current game."""
        log.info('Request to close game')
        if not self.context.in_game:
            log.info('No game to close')
            return


    def do_quit(self):
        """Quit the application."""
        log.info('Request to quit')
        self.event_bus.emit(Events.action_quit)


    # -- Preferences retrieval / setting

    def get_gui_wait_time(self) -> int:
        """Get the GUI wait validation time."""
        log.debug('Getting GUI wait validation time')
        return settings.gui.wait_validate

    # -- Private methods


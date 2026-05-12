# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

from pytrisk.controller.game     import GameController
from pytrisk.controller.main     import MainController
from pytrisk.controller.startup  import StartupController
from pytrisk.logger import log


class Controller:
    """
    Controller that dispatches events to subcontrollers. It is totally
    transparent for the rest of the application.
    """
    def __init__(self, context, event_bus):
        # subcontrollers
        self._controllers = [
            MainController(self, context, event_bus),
            StartupController(self, context, event_bus),
            GameController(self, context, event_bus)
        ]

    def __getattr__(self, name):
        """Dispatch events to subcontrollers automatically."""
        for controller in self._controllers:
            if hasattr(controller, name):
                log.debug(f'Found method {name} in {controller.__class__.__name__}')
                return getattr(controller, name)

        raise AttributeError(name)


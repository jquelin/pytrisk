# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import tkinter as tk

from pytrisk.locale    import _
from pytrisk.logger    import log
from pytrisk.ui.views.game_canvas import GameCanvasView


class GameView(tk.Frame):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent)

        # Subscribe to events & store the controller for later use.
        event_bus.subscribe(self)
        self.controller = controller
        self.event_bus  = event_bus

        # GUI creation
        log.info('Creating game frame')
        self._create_views()

    # -- Private methods

    def _create_views(self):
        """Create the various views and assemble them."""
        controller = self.controller
        event_bus  = self.event_bus

        # Create the game canvas
        canvas = GameCanvasView(self, controller, event_bus)
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    # -- Private methods

    # -- Event handlers



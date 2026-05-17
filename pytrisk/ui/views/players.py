# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import tkinter as tk

from pytrisk.locale    import _
from pytrisk.logger    import log

class PlayersView(tk.LabelFrame):
    def __init__(self, parent, controller, event_bus):
        log.info('Creating players frame')
        super().__init__(parent, text=' ' + _('Players') + ' ')

        # Subscribe to events & store the controller for later use.
        event_bus.subscribe(self)
        self.controller = controller

        # Create ui
        self._create_ui()


    # -- Private methods

    def _create_ui(self):
        """Create the ui."""

        subframe = tk.Frame(self,bg='yellow')
        subframe.pack(side=tk.TOP, padx=5, pady=5, expand=True)

        for p in self.controller.get_players():
            f = tk.Frame(subframe, width=16, height=16, bg=p.color)
            f.pack(side=tk.LEFT)


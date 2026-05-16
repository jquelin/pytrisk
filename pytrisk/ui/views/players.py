# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import tkinter as tk

from pytrisk.locale    import _
from pytrisk.logger    import log

class PlayersView(tk.LabelFrame):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent, text=' ' + _('Players') + ' ')

        # Subscribe to events & store the controller for later use.
        event_bus.subscribe(self)
        self.controller = controller

        a = tk.Label(self, text='a')
        a.pack()

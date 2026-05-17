# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import tkinter as tk
from tkinter import ttk

from pytrisk.locale    import _
from pytrisk.logger    import log
from pytrisk.ui.widgets.scroll_frame import ScrolledFrame

class ContinentsView(tk.LabelFrame):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent, text=' ' + _('Continents') + ' ')
        log.info('Creating continents frame')

        # Subscribe to events & store the controller for later use.
        event_bus.subscribe(self)
        self.controller = controller

        # GUI creation
        self._create_table()


    # -- Private methods

    def _create_table(self):
        frame = ScrolledFrame(self)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.inner = frame.inner

        headers = [
            (_("Continent"), tk.W),
            (_("Bonus"), tk.CENTER),
            (_("# Countries"), tk.CENTER),
        ]

        font = ("TkDefaultFont", 8)

        # First create the headers
        bg_header    = "#b0b0b0"
        bg_continent = "#c5c5c5"
        for col, (text, anchor) in enumerate(headers):
            label = tk.Label(self.inner, text=text, bg=bg_header,
                             relief="raised",
                             borderwidth=1,
                             anchor=anchor,
                             font=font)
            label.grid(row=0, column=col, sticky="nsew", )

        # Then create the continents (sorted by bonus, then by name)
        continents = sorted(
            self.controller.get_continents(),
            key=lambda c: (-c.bonus, c.name))
        for idx, continent in enumerate(continents):
            label = tk.Label(self.inner, text=continent.name, anchor=tk.W,
                bg=bg_continent, relief="raised", font=font)
            label.grid(row=1+idx, column=0, sticky="nsew")

            label = tk.Label(self.inner, text=continent.bonus,
                bg=bg_continent, relief="raised", font=font)
            label.grid(row=1+idx, column=1, sticky="nsew")

            label = tk.Label(self.inner, text=len(continent.countries),
                bg=bg_continent, relief="raised", font=font)
            label.grid(row=1+idx, column=2, sticky="nsew")

        # Finally create the players
        players = self.controller.get_players()
        for player in players:
            label = tk.Label(self.inner, bg=player.color, relief="raised", width=3)
            label.grid(row=0, column=3+player.index, sticky="nsew")
            for i in range(len(continents)):
                label = tk.Label(self.inner, text="0", borderwidth=1,
                                 relief='sunken', font=font)
                label.grid(row=1+i, column=3+player.index, sticky="nsew")




    # -- Public methods: event bus handlers

    def on_player_add(self, idx, player):
        log.info(f'Adding player {idx}')

        # Add the player header
        label = tk.Label(self.inner, bg=player.color,
                             relief="raised",
                             borderwidth=1)
        label.grid(row=0, column=3+idx)


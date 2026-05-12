# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import tkinter as tk

class StatusbarView(tk.Frame):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent)
        event_bus.subscribe(self)

        # Sunken inner frame to hold the widgets
        f = tk.Frame(self, relief=tk.SUNKEN, borderwidth=1)
        f.pack(side=tk.TOP, fill=tk.X, expand=True)

        # Label to display status
        statuslab = tk.Label(f, anchor=tk.W)
        statuslab.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1, pady=1)

        # Label to display country pointed by mouse
        countrylab= tk.Label(f, anchor=tk.E)
        countrylab.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=1, pady=1)

        # Dictionary to map status level to label
        self._targets = {
            'info': statuslab,
            'error': statuslab,
            'hint':  countrylab,
        }


    # -- Public methods: event bus handlers

    def on_status_clear(self, level):
        """Clear the status message in the relevant label.

        args:
            level (str): 'info', 'error', 'hint'
        """
        self._targets[level].config(text='')

    def on_status_message(self, level, message):
        """Set the status message in the relevant label.

        args:
            level (str): 'info', 'error', 'hint'
            message (str): message to display
        """
        self._targets[level].config(text=message)
        if level == 'error':
            self._targets[level].config(fg='red')
        else:
            self._targets[level].config(fg='black')


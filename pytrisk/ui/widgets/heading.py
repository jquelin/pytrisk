# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import tkinter as tk

class Heading(tk.Frame):
    """A heading widget."""

    def __init__(self, parent, text):
        super().__init__(parent)

        # Create the label
        lab = tk.Label(self, text=text)
        lab = tk.Label(self, text=text,
                       bg='black', fg='white',
                       font=('TkDefaultFont', 14, 'bold'))
        lab.pack(side=tk.TOP, fill=tk.X, padx=20, pady=20)

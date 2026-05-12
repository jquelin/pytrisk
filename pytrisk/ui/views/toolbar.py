# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk  as ttk
from TkToolTip import ToolTip

from pytrisk.locale   import _
from pytrisk.ui.utils import Icons

class ToolbarView(tk.Frame):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent)

        self.controller = controller

        icon = Icons.load('quit')
        but = tk.Button(self, image=icon, command=self._on_quit)
        but.pack(side=tk.LEFT)
        tooltip = ToolTip(but, msg=_('Quit'))

        icon = Icons.load('close')
        but = tk.Button(self, image=icon, state=tk.DISABLED,
                        command=self._on_nothing)
        but.pack(side=tk.LEFT)
        tooltip = ToolTip(but, msg=_('Close'))

        sep = ttk.Separator(self, orient=tk.VERTICAL)
        sep.pack(side=tk.LEFT, fill=tk.Y, padx=4, pady=4)

        font_bold = tkfont.Font(font='TkDefaultFont')
        font_bold.config(weight='bold')
        lab = tk.Label(self, text=_('Game state:'), font=font_bold)
        lab.pack(side=tk.LEFT)

        lab = tk.Label(self, text=_('place armies'), state=tk.DISABLED)
        lab.pack(side=tk.LEFT)

        icon = Icons.load('undo')
        but = tk.Button(self, image=icon, state=tk.DISABLED,
                        command=self._on_nothing)
        but.pack(side=tk.LEFT)
        tooltip = ToolTip(but, msg=_('undo all'))

        icon = Icons.load('next')
        but = tk.Button(self, image=icon, state=tk.DISABLED,
                        command=self._on_nothing)
        but.pack(side=tk.LEFT)
        tooltip = ToolTip(but, msg=_('ready for attack'))

        lab = tk.Label(self, text=_('attack'), state=tk.DISABLED)
        lab.pack(side=tk.LEFT)

        icon = Icons.load('redo')
        but = tk.Button(self, image=icon, state=tk.DISABLED,
                        command=self._on_nothing)
        but.pack(side=tk.LEFT)
        tooltip = ToolTip(but, msg=_('attack again'))

        icon = Icons.load('next')
        but = tk.Button(self, image=icon, state=tk.DISABLED,
                        command=self._on_nothing)
        but.pack(side=tk.LEFT)
        tooltip = ToolTip(but, msg=_('consolidate'))

        lab = tk.Label(self, text=_('move armies'), state=tk.DISABLED)
        lab.pack(side=tk.LEFT)

        icon = Icons.load('stop')
        but = tk.Button(self, image=icon, state=tk.DISABLED,
                        command=self._on_nothing)
        but.pack(side=tk.LEFT)
        tooltip = ToolTip(but, msg=_('turn finished'))




    # Private methods: tk callbacks

    def _on_nothing(self):
        pass

    def _on_quit(self):
        """Request the controller to quit the application."""
        self.controller.do_quit()

#
# This file is part of pytrisk.
#
# pytrisk is free software: you can redistribute it and/or modify it
# under the # terms of the GNU General Public License as published by
# the Free Software # Foundation, either version 3 of the License, or
# (at your option) any later # version.
#
# pytrisk is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with pytrisk. If not, see <https://www.gnu.org/licenses/>.
#

import tkinter as tk
from tkinter import ttk

from pytrisk.locale import _
from pytrisk.logger import log
from pytrisk.ui.utils import Icons


class ColorSelector(tk.Frame):
    """A color selector grid with icon overlay on selected color.

    Args:
        parent: parent widget
        colors: list of available colors
        initial: initial selected color
        nbcols: number of columns (default: 5)
    """

    def __init__(self, parent, colors, initial, nbcols=5):
        super().__init__(parent)

        # Prepare color selector
        self._color_var = tk.StringVar(value=initial)
        self._color_buttons = {}
        self._icon = Icons.load('player-active')

        # Build selector
        size = 16
        for idx, color in enumerate(colors):
            row = idx // nbcols
            col = idx % nbcols
            btn = tk.Frame(self, width=size, height=size,
                           bg=color, relief=tk.RAISED, bd=1)
            btn.grid(row=row, column=col)
            btn.bind('<Button-1>', lambda e, c=color: self._select_color(c))
            btn.color = color

            self._color_buttons[color] = btn

        # Update color display
        self._select_color(initial)


    def _select_color(self, color):
        """Select a color."""
        self._color_var.set(color)
        selected = self._color_var.get()
        for color, btn in self._color_buttons.items():
            for child in btn.winfo_children():
                child.destroy()
            if color == selected:
                lbl = tk.Label(btn, image=self._icon, bg=color)
                lbl.image = self._icon
                lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # -- Public methods

    def get_color(self):
        """Return the selected color."""
        return self._color_var.get()

    def enable(self):
        """Enable the color selector buttons."""
        for btn in self._color_buttons.values():
            btn.bind('<Button-1>', lambda e, c=btn.color: self._select_color(c))
            btn.configure(cursor='hand2')

    def disable(self):
        """Disable the color selector buttons."""
        for btn in self._color_buttons.values():
            btn.unbind('<Button-1>')
            btn.configure(cursor='')


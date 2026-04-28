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

import colorsys
import tkinter as tk
from tkinter import ttk

from pytrisk.ui.utils import Icons


class ColorSelector(tk.Frame):
    def __init__(self, parent, colors, initial, command=None, nbcols=5):
        super().__init__(parent)

        # store variables
        self._colors  = colors
        self._nbcols  = nbcols
        self._command = command
        self._color   = initial
        self._popup   = None

        # create main button
        self._button = tk.Button(self,
            bg               = initial,
            activebackground = initial,
            command          = self._toggle_popup,
            image            = Icons.load('paintbrush')
        )
        self._button.pack()


    # -- Private methods: popup management

    def _toggle_popup(self):
        if self._popup and self._popup.winfo_exists():
            self._close_popup()
        else:
            self._open_popup()

    def _open_popup(self):
        if self._popup:
            return

        # create a toplevel window with no border
        self._popup = tk.Toplevel(self)
        self._popup.overrideredirect(True)

        # position at the right of the button
        x = self._button.winfo_rootx() + self._button.winfo_width()
        y = self._button.winfo_rooty()
        self._popup.geometry(f"+{x}+{y}")

        # construct the grid
        size = 16
        for idx, color in enumerate(self._colors):
            row = idx // self._nbcols
            col = idx % self._nbcols
            f = tk.Frame(self._popup, width=size, height=size, bg=color)
            f.grid(row=row, column=col)
            f.bind('<Button-1>', lambda e, c=color: self._on_color_selected(c))

        # close if clicked outside
        self.winfo_toplevel().bind('<Button-1>', self._click_outside)


    def _close_popup(self):
        if self._popup:
            self._popup.destroy()
            self._popup = None
            self.winfo_toplevel().unbind('<Button-1>')

    def _click_outside(self, event):
        if not self._popup:
            return

        widget = event.widget
        if widget is self._button:
            return

        if str(widget).startswith(str(self._popup)):
            return

        self._close_popup()


    # -- Private method: selection

    def _on_color_selected(self, color):
        # ignore if already selected
        if self._color == color:
            self._close_popup()
            return

        # store new color, update and close popup
        self._color = color
        self._button.configure(bg=color, activebackground=color)
        self._close_popup()

        # callback if any
        if self._command:
            self._command(color)

    def _desaturate(self, color, factor=0.1):
        """Return a desaturated version of a Tk color."""
        r, g, b = self.winfo_rgb(color)
        r /= 65535
        g /= 65535
        b /= 65535

        h, l, s = colorsys.rgb_to_hls(r, g, b)
        s *= factor  # reduce saturation

        r, g, b = colorsys.hls_to_rgb(h, l, s)

        return "#%02x%02x%02x" % (int(r*255), int(g*255), int(b*255))

    # -- Public API

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color.set(color)
        self._button.configure(bg=color, activebackground=color)

    def enable(self):
        self._button.configure(state=tk.NORMAL, bg=self._color)

    def disable(self):
        self._button.configure(state=tk.DISABLED, bg=self._desaturate(self._color))

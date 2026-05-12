# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import colorsys
import tkinter as tk
from tkinter import ttk

from pytrisk.ui.utils import Icons


class ColorSelector(tk.Frame):
    """A Tkinter widget for selecting a color from a predefined palette.

    Displays a button showing the currently selected color. Clicking the button
    opens a popup window with a grid of available colors. Selecting a color
    updates the button appearance and triggers an optional callback.
    """

    def __init__(self, parent, colors, initial, command=None, nbcols=5):
        """Initialize the ColorSelector widget.

        Note that if command is provided, ColorSelector will *not* update the
        button appearance. You will be responsible to set it via `set_color()`.

        Args:
            parent: The parent Tkinter widget.
            colors: List of color strings (e.g., '#ff0000', 'red') available for selection.
            initial: The initial selected color (should be present in colors).
            command: Optional callback function invoked with the selected color as argument when a new color is chosen.
            nbcols: Number of columns in the color grid popup (default: 5).
        """
        super().__init__(parent)

        # store variables
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
        """Toggle the visibility of the color selection popup.

        Closes the popup if it is currently open, otherwise opens it.
        """
        if self._popup and self._popup.winfo_exists():
            self._close_popup()
        else:
            self._open_popup()

    def _open_popup(self):
        """Open the color selection popup.

        Creates a borderless Toplevel window positioned to the right of the main
        button, containing a grid of color swatches. Binds a global click handler
        to close the popup when clicking outside of it or the button.
        """
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
            f = tk.Frame(self._popup, width=size, height=size, bg=color, cursor='hand2')
            f.grid(row=row, column=col)
            f.bind('<Button-1>', lambda e, c=color: self._on_color_selected(c))

        # close if clicked outside
        self.winfo_toplevel().bind('<Button-1>', self._click_outside)


    def _close_popup(self):
        """Close and destroy the color selection popup.

        Destroys the popup window and unbinds the global click handler used to
        detect outside clicks.
        """
        if self._popup:
            self._popup.destroy()
            self._popup = None
            self.winfo_toplevel().unbind('<Button-1>')

    def _click_outside(self, event):
        """Handle click events to close the popup when clicking outside.

        Args:
            event: The Tkinter Button-1 event object.
        """
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
        """Handle selection of a color swatch from the popup grid.

        Updates the current color, refreshes the main button appearance, closes
        the popup, and invokes the callback function if the selected color is new.

        Args:
            color: The color string selected by the user.
        """
        # ignore if already selected
        if self._color == color:
            self._close_popup()
            return

        # close popup
        self._close_popup()

        # callback if any, otherwise proceed with color change
        if self._command:
            self._command(color)
        else:
            self.set_color(color)

    def _desaturate(self, color, factor=0.1):
        """Return a desaturated version of a Tk color string.

        Converts the input color to RGB, transforms to HLS color space to reduce
        saturation, then converts back to a hex color string.

        Args:
            color: Tk color string (e.g., '#ff0000', 'red').
            factor: Saturation multiplier (0.0 to 1.0). Lower values produce more desaturated colors (default: 0.1).

        Returns:
            Desaturated color as a hex string (e.g., '#cc3333').
        """
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
        """Return the currently selected color string."""
        return self._color

    def set_color(self, color):
        """Set the currently selected color and update the button.

        Args:
            color: The new color string to select.
        """
        self._color = color
        self._button.configure(bg=color, activebackground=color)

    def enable(self):
        """Enable the color selector button, allowing user interaction."""
        self._button.configure(state=tk.NORMAL, bg=self._color)

    def disable(self):
        """Disable the color selector button and desaturate its background."""
        self._button.configure(state=tk.DISABLED, bg=self._desaturate(self._color))

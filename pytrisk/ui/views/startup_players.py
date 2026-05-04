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
from pytrisk.ui.widgets.color_selector import ColorSelector


class StartupPlayerDefinition(tk.Frame):
    def __init__(self, parent, controller, event_bus, index):
        super().__init__(parent)
        self.controller = controller
        self.event_bus  = event_bus
        self.index      = index

        # Subscribe to events
        event_bus.subscribe(self)

        # Color selector at the right
        all_colors = controller.get_available_player_colors()
        initial_color = controller.get_default_player_color(index)
        self.color_selector = ColorSelector(self, all_colors, initial_color,
                                            command=self._on_color_selected)
        self.color_selector.pack(side=tk.RIGHT, padx=6)


    # -- tk events

    def _on_color_selected(self, color):
        log.info(f'User wants to change player {self.index} color to {color}')
        self.controller.set_player_color(self.index, color)

    # -- Controller events

    def on_player_color_changed(self, index, color):
        """Called when the color of a player has changed."""
        if index != self.index:
            return
        log.info(f'Player {index} color changed to {color}')
        self.color_selector.set_color(color)


class StartupHumanPlayerDefinition(StartupPlayerDefinition):
    """A human player row: static label + editable name entry + color selector."""

    def __init__(self, parent, controller, event_bus):
        # human player is always at index 0
        super().__init__(parent, controller, event_bus, 0)

        lab = tk.Label(self, text=_('Human player'), width=12, anchor=tk.W)
        lab.pack(side=tk.LEFT)

        self.name_var = tk.StringVar()
        default_name = controller.get_player_name(0)
        self.name_var.set(default_name)
        self.name_entry = ttk.Entry(self, textvariable=self.name_var)
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)


class StartupAIPlayerDefinition(StartupPlayerDefinition):
    """An AI player row: label with difficulty selector + color selector.

    Args:
        parent: parent widget
        index: index number for this AI player (1, 2, 3, ...)
    """

    def __init__(self, parent, controller, event_bus, index: int):
        super().__init__(parent, controller, event_bus, index)

        # Label
        ai_label = _('AI player') + f' {index}'
        lab = tk.Label(self, text=ai_label, width=12, anchor=tk.W)
        lab.pack(side=tk.LEFT)

        # Difficulty setting
        self.difficulty_var = tk.StringVar()
        self.difficulty_cb = ttk.Combobox(
            self,
            values=[_('Easy'), _('Hard')],
            textvariable=self.difficulty_var,
            width=8,
            state='readonly'
        )
        self.difficulty_cb.set(_('Easy'))
        self.difficulty_cb.pack(side=tk.LEFT, padx=6)


    def enable(self):
        """Enable the difficulty combobox and color selector."""
        self.difficulty_cb.configure(state='readonly')
        self.color_selector.enable()

    def disable(self):
        """Disable the difficulty combobox and color selector (keep the row visible)."""
        self.difficulty_cb.configure(state=tk.DISABLED)
        self.color_selector.disable()

    def get_difficulty(self):
        """Return the difficulty ('Easy' or 'Hard')."""
        return self.difficulty_var.get()


class StartupPlayersView(tk.LabelFrame):
    """View to select players and number of players.

    It shows up to 6 player rows. The first player is always human (editable
    name). The following players are AI with a difficulty selector (Easy/Hard).
    The user can choose the number of players (2..6) using a spin control.
    When the number of players is changed, rows for existing players are enabled
    (state normal) and the extra rows are disabled (state disabled) but not
    removed.
    """

    def __init__(self, parent, controller, event_bus):
        super().__init__(parent, text=_(' Players '), labelanchor=tk.N)

        event_bus.subscribe(self)
        self.controller = controller
        self.event_bus  = event_bus

        # Number of players variable
        self._nb_players = tk.IntVar(value=2)

        # Header with spinbox to select number of players
        hdr = tk.Frame(self)
        hdr.pack(side=tk.TOP, fill=tk.X, padx=6, pady=6)

        lab = tk.Label(hdr, text=_('Number of players:'))
        lab.pack(side=tk.LEFT)

        # Use a small spinbox for selecting 2..6
        sp = tk.Spinbox(hdr, from_=2, to=6, width=3, textvariable=self._nb_players)
        sp.pack(side=tk.LEFT, padx=6)

        # Trace changes to number of players
        try:
            # modern tkinter
            self._nb_players.trace_add('write', self._on_nb_players_change)
        except Exception:
            # fallback
            self._nb_players.trace('w', self._on_nb_players_change)

        # Allow controlling the spinbox with the mouse wheel across platforms.
        # - Windows & macOS: <MouseWheel> with event.delta > 0 or < 0
        # - X11 (many Linux): <Button-4> (up) and <Button-5> (down)
        sp.bind('<MouseWheel>', self._on_spinbox_mousewheel)
        sp.bind('<Button-4>', self._on_spinbox_mousewheel)
        sp.bind('<Button-5>', self._on_spinbox_mousewheel)

        # Create the rows: first is human, the rest are AI
        self._rows = []  # list of StartupPlayerDefinition instances

        body = tk.Frame(self)
        body.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Human player (always first)
        human = StartupHumanPlayerDefinition(body, controller, event_bus)
        human.pack(side=tk.TOP, fill=tk.X, pady=2)
        self._rows.append(human)

        # AI players
        for i in range(1, 6):
            ai = StartupAIPlayerDefinition(body, controller, event_bus, i)
            ai.pack(side=tk.TOP, fill=tk.X, pady=2)
            self._rows.append(ai)

        # Initialize rows state according to initial nb players
        self._update_rows()

    # -- Private methods

    def _on_nb_players_change(self, *args):
        """Callback when the spinbox number changes."""
        try:
            n = int(self._nb_players.get())
        except Exception:
            log.warning('invalid number of players')
            return

        if n < 2:
            n = 2
            self._nb_players.set(n)
        if n > 6:
            n = 6
            self._nb_players.set(n)

        log.info(f'number of players set to {n}')
        self._update_rows()

    def _on_spinbox_mousewheel(self, event):
        """Handle mouse wheel events on the spinbox in a cross-platform way.

        Return "break" to stop propagation so the main window doesn't scroll
        or receive the same wheel event.
        """
        try:
            cur = int(self._nb_players.get())
        except Exception:
            cur = 2

        # X11 mouse wheel events use Button-4/5
        delta = 0
        if hasattr(event, 'num') and event.num in (4, 5):
            delta = 1 if event.num == 4 else -1
        else:
            # Windows and macOS: event.delta positive/negative
            try:
                delta = 1 if event.delta > 0 else -1
            except Exception:
                delta = 0

        if delta == 0:
            return "break"

        new = cur + delta
        if new < 2:
            new = 2
        if new > 6:
            new = 6

        if new != cur:
            # Setting the IntVar triggers the trace handler which updates rows
            self._nb_players.set(new)

        # prevent other handlers from also processing the event
        return "break"

    def _update_rows(self):
        """Enable or disable rows depending on the selected number of players.

        Rows beyond the selected number are kept visible but disabled.
        """
        n = int(self._nb_players.get())

        # AI players: first (n-1) are enabled, rest disabled
        for idx in range(1, 6):
            if idx < n:
                self._rows[idx].enable()
            else:
                self._rows[idx].disable()

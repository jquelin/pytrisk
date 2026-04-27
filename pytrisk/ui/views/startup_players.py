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


class StartupPlayerDefinition(tk.Frame):
    """A single player row: human player (name) or AI player (difficulty).

    Provides enable() / disable() methods to change the state of contained
    widgets without the parent needing to track them individually.

    Args:
        parent: parent widget
        idx: player index (1 = human, 2+ = AI)
    """

    def __init__(self, parent, idx: int):
        super().__init__(parent)

        self.idx = idx
        is_human = (idx == 1)

        if is_human:
            # Human player: static label + editable name
            lab = tk.Label(self, text=_('Human player'), width=12, anchor=tk.W)
            lab.pack(side=tk.LEFT)

            self.name_var = tk.StringVar()
            default_name = _('Player')
            self.name_var.set(default_name)
            self.name_entry = ttk.Entry(self, textvariable=self.name_var)
            self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)

            # No difficulty for human
            self.difficulty_cb = None
        else:
            # AI player: label with index + difficulty selector
            ai_label = _('AI player') + f' {idx - 1}'
            lab = tk.Label(self, text=ai_label, width=12, anchor=tk.W)
            lab.pack(side=tk.LEFT)

            # No name entry for AI
            self.name_var = None
            self.name_entry = None

            # Difficulty combobox
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
        """Enable this player row."""
        if self.name_entry is not None:
            self.name_entry.configure(state=tk.NORMAL)
        if self.difficulty_cb is not None:
            self.difficulty_cb.configure(state='readonly')

    def disable(self):
        """Disable this player row (keeps it visible)."""
        if self.name_entry is not None:
            self.name_entry.configure(state=tk.DISABLED)
        if self.difficulty_cb is not None:
            self.difficulty_cb.configure(state=tk.DISABLED)


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

        for i in range(1, 7):
            row = StartupPlayerDefinition(body, i)
            row.pack(side=tk.TOP, fill=tk.X, pady=2)
            self._rows.append(row)

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

        for idx, r in enumerate(self._rows, start=1):
            if idx <= n:
                r.enable()
            else:
                r.disable()
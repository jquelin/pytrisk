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


class StartupPlayersView(tk.LabelFrame):
    """View to select players and number of players.

    It shows up to 6 player rows. The first player is always human. The
    following players default to AI. The user can choose the number of
    players (2..6) using a spin control. When the number of players is
    changed, rows for existing players are enabled (state normal) and the
    extra rows are disabled (state disabled) but not removed.
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

        # Create the rows for up to 6 players
        self._rows = []  # list of dicts {frame, name_entry, type_cb}

        body = tk.Frame(self)
        body.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=6, pady=6)

        for i in range(1, 7):
            row = tk.Frame(body)
            row.pack(side=tk.TOP, fill=tk.X, pady=2)

            # Player label
            labp = tk.Label(row, text=f'{_('Player')} {i}:', width=10, anchor=tk.W)
            labp.pack(side=tk.LEFT)

            # Name entry
            name_var = tk.StringVar()
            default_name = _('Player') + f' {i}' if i == 1 else _('AI') + f' {i-1}'
            name_var.set(default_name)
            name_entry = ttk.Entry(row, textvariable=name_var)
            name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)

            # Type combobox (Human / AI)
            type_cb = ttk.Combobox(row, values=[_('Human'), _('AI')], width=8, state='readonly')
            if i == 1:
                type_cb.set(_('Human'))
                # first player always human and not editable
                type_cb.configure(state='disabled')
            else:
                type_cb.set(_('AI'))

            type_cb.pack(side=tk.LEFT, padx=6)

            self._rows.append({
                'frame': row,
                'name_var': name_var,
                'name_entry': name_entry,
                'type_cb': type_cb,
            })

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

    def _update_rows(self):
        """Enable or disable rows depending on the selected number of players.

        Rows beyond the selected number are kept visible but disabled.
        """
        n = int(self._nb_players.get())

        for idx, r in enumerate(self._rows, start=1):
            name_entry = r['name_entry']
            type_cb = r['type_cb']

            if idx <= n:
                # enable
                name_entry.configure(state=tk.NORMAL)
                # first player's type combobox remains disabled (always human)
                if idx == 1:
                    type_cb.configure(state=tk.DISABLED)
                    type_cb.set(_('Human'))
                else:
                    # allow selecting AI/human if desired
                    type_cb.configure(state=tk.READONLY)
            else:
                # disable but keep visible
                name_entry.configure(state=tk.DISABLED)
                # keep combobox disabled as well
                type_cb.configure(state=tk.DISABLED)

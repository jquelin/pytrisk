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

from dataclasses import dataclass
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

from pytrisk.locale    import _
from pytrisk.logger    import log
from pytrisk.ui.views.startup_maps import StartupMapsView
from pytrisk.ui.views.startup_players import StartupPlayersView
from pytrisk.ui.widgets.heading    import Heading



class StartupView(tk.Frame):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent)

        # Subscribe to events & store the controller for later use.
        event_bus.subscribe(self)
        self.controller = controller
        self.event_bus  = event_bus

        # GUI creation
        log.info('creating startup frame')
        self._create_views()


    def _create_views(self):
        """Create the various views and assemble them."""
        controller = self.controller
        event_bus  = self.event_bus

        # The view heading
        heading = Heading(self, text=_('New game'))
        heading.pack(side=tk.TOP, fill=tk.X)

        # The button to actually start the new game
        but = tk.Button(self, text=_('Start'), bg='black', fg='white',
                        command=self._on_btn_start_click)
        but.pack(side='bottom', fill=tk.X, padx=10, pady=10)

        # Create the maps view
        fmaps = StartupMapsView(self, controller, event_bus)
        fmaps.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        # Create the players view
        fplayers = StartupPlayersView(self, controller, event_bus)
        fplayers.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=10)


    # -- Private methods

    def _on_btn_start_click(self):
        """Request to start a new game."""
        log.info('user wants to start new game')
        self.controller.do_start_new_game()


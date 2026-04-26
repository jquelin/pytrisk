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

        lab = tk.Label(self, text=_('New game'), bg='black', fg='white', font=('TkDefaultFont', 14, 'bold'))
        lab.pack(side=tk.TOP, fill=tk.X, padx=20, pady=20)

        # Create the maps view
        fmaps = StartupMapsView(self, controller, event_bus)
        fmaps.pack(side=tk.LEFT, fill=tk.Y, expand=False)


    # -- Private methods


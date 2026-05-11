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

from pytrisk.locale    import _
from pytrisk.logger    import log
from pytrisk.ui.views.game_canvas import GameCanvasView


class GameView(tk.Frame):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent)

        # Subscribe to events & store the controller for later use.
        event_bus.subscribe(self)
        self.controller = controller
        self.event_bus  = event_bus

        # GUI creation
        log.info('Creating game frame')
        self._create_views()


    def _create_views(self):
        """Create the various views and assemble them."""
        controller = self.controller
        event_bus  = self.event_bus

        # Create the game canvas
        canvas = GameCanvasView(self, controller, event_bus)
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    # -- Private methods

    # -- Event handlers



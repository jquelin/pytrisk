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

from pathlib import Path
import tkinter as tk
from tkinter import ttk

from pytrisk.config import config
import pytrisk.data
from pytrisk.locale    import _
from pytrisk.logger    import log
from pytrisk.constants import appinfo
from pytrisk.ui.utils              import Icons
from pytrisk.ui.views.menu         import MenuView
from pytrisk.ui.views.startup      import StartupView
from pytrisk.ui.views.statusbar    import StatusbarView
from pytrisk.ui.views.toolbar      import ToolbarView


class MainWindow(tk.Tk):
    def __init__(self, controller, event_bus):
        super().__init__()

        # Subscribe to events & store the controller for later use.
        event_bus.subscribe(self)
        self.controller = controller
        self.event_bus  = event_bus

        # GUI creation
        log.info('creating main window')
        self.title(appinfo.title)
        self.iconphoto(True, Icons.load(appinfo.name))
        self._create_views()

        # Add some bindings
        self.protocol('WM_DELETE_WINDOW', self._on_quit)
        self.bind('<Control-q>', self._on_quit)


    # -- gui construction

    def _create_views(self):
        """Create the various views and assemble them."""
        controller = self.controller
        event_bus  = self.event_bus

        # GUI elements always present
        menu = MenuView(self, controller, event_bus)
        self.config(menu=menu)

        toolbar = ToolbarView(self, controller, event_bus)
        toolbar.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5)

        statusbar = StatusbarView(self, controller, event_bus)
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Startup view
        startup_frame = StartupView(self, self.controller, self.event_bus)
        startup_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)


    def _build_startup_frame(self):
        f_players = tk.Frame(frame)
        f_players.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        lab = tk.Label(f_players, text=_('Players'))
        lab.pack(side=tk.TOP)
        f = tk.Frame(f_players)
        f.pack(side=tk.TOP, fill=tk.X)
        lab = tk.Label(f, text=_('Number of players'))
        lab.pack(side=tk.LEFT)
        scale = tk.Scale(f, orient=tk.HORIZONTAL, from_=2, to=10)
        scale.set(3)
        scale.pack(side=tk.LEFT, fill=tk.X)



    # -- Controller events

    def on_action_quit(self):
        """Actually quit the application."""
        self.destroy()


    # -- gui callbacks

    def _on_quit(self, event=None):
        """Signal the controller we want to quit the application."""
        self.controller.do_quit()


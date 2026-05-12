# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import tkinter as tk

from pytrisk.locale    import _
from pytrisk.logger    import log
from pytrisk.constants import appinfo
from pytrisk.ui.utils            import Icons
from pytrisk.ui.views.game       import GameView
from pytrisk.ui.views.menu       import MenuView
from pytrisk.ui.views.startup    import StartupView
from pytrisk.ui.views.statusbar  import StatusbarView
from pytrisk.ui.views.toolbar    import ToolbarView

class MainWindow(tk.Tk):
    def __init__(self, controller, event_bus):
        super().__init__()

        # Subscribe to events & store the controller for later use.
        event_bus.subscribe(self)
        self.controller = controller
        self.event_bus  = event_bus

        # GUI creation
        log.info('creating main window')
        self.withdraw()
        self.title(appinfo.title)
        icon = Icons.load(appinfo.name)
        self.iconphoto(True, icon)
        self._create_views()
        self._lock_window()


    # -- gui construction

    def _create_bindings(self):
        """Create the global bindings for the main window."""
        # Add some bindings
        self.protocol('WM_DELETE_WINDOW', self._on_quit)
        self.bind_all('<Control-q>', self._on_quit)
        self.bind_all('<Control-w>', self._on_close)


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
        self.startup_frame = startup_frame


    def _lock_window(self):
        """Lock the window to its current size."""
        # Ensure minimum window size
        self.update_idletasks()
        self.pack_propagate(False) # prevent main window from being resized by other widgets
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        self.geometry(f"{w}x{h}")
        self.minsize(w, h)
        self.deiconify()
        self.lift()                # raise the window
        self.focus_force()


    # -- Controller events

    def on_action_quit(self):
        """Actually quit the application."""
        log.info('Quitting application')
        self.destroy()


    def on_new_game(self):
        """Close the startup frame when a new game is started."""
        log.info('Closing startup frame')
        self.startup_frame.destroy()
        log.info('Creating game frame')
        game_frame = GameView(self, self.controller, self.event_bus)
        game_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.game_frame = game_frame



    # -- gui callbacks

    def _on_close(self, _):
        """Signal the controller we want to close the current game."""
        self.controller.do_close_game()

    def _on_quit(self, event=None):
        """Signal the controller we want to quit the application."""
        self.controller.do_quit()


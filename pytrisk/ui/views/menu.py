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

from pytrisk.config   import config
from pytrisk.locale   import _
from pytrisk.logger   import log
from pytrisk.ui.utils import Icons

class MenuView(tk.Menu):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent)

        self.controller = controller
        event_bus.subscribe(self)

        # Variables holding misc stuff
        self._menus   = {}
        self._indexes = {}
        self._vars    = {}

        # Create the menus
        self._create_menu_game()
        self._create_menu_view()
        self._create_menu_actions()


    # -- Private methods

    def _create_menu_game(self):
        # Menu: game
        menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label=_('Game'), underline=0, menu=menu)
        self._menus["game"]   = menu
        self._indexes["game"] = {}

        label = _('Close')
        icon  = Icons.load('close')
        menu.add_command(
                label=label, underline=0, accelerator='Ctrl+W',
                image=icon, compound=tk.LEFT,
                state=tk.DISABLED, command=self._on_close)
        self._indexes["game"]["close"] = menu.index(tk.END)

        menu.add_separator()

        icon  = Icons.load('quit')
        menu.add_command(
                label=_('Quit'), underline=0, accelerator='Ctrl+Q',
                image=icon, compound=tk.LEFT,
                command=self._on_quit)


    def _create_menu_view(self):
        # Menu: view
        menu = tk.Menu(self, tearoff=False)
        self._menus["view"]   = menu
        self._indexes["view"] = {}
        self.add_cascade(label=_('View'), underline=0, menu=menu)

        label = _('Maintain aspect ratio')
        self._vars["ratio"] = tk.BooleanVar(value=config.get('gui.aspect.keep_ratio'))
        menu.add_checkbutton(label=label, underline=0,
                variable=self._vars["ratio"],
                compound=tk.LEFT, state=tk.DISABLED,
                command=self._on_mnu_view_ratio
        )
        self._indexes["view"]["ratio"] = menu.index(tk.END)


    def _create_menu_actions(self):
        # Menu: actions
        menu = tk.Menu(self, tearoff=False)
        self._menus["actions"] = menu

        self.add_cascade(label=_('Actions'), underline=0, menu=menu)
        label = _('Undo all')
        icon  = Icons.load('undo')
        menu.add_command(
                label=label, underline=0, accelerator='u',
                image=icon, compound=tk.LEFT,
                state=tk.DISABLED, command=self._on_close)
        label = _('Attack')
        icon  = Icons.load('next')
        menu.add_command(
                label=label, underline=0, accelerator='a',
                image=icon, compound=tk.LEFT,
                state=tk.DISABLED, command=self._on_close)
        label = _('Re-attack')
        icon  = Icons.load('redo')
        menu.add_command(
                label=label, underline=0, accelerator='r',
                image=icon, compound=tk.LEFT,
                state=tk.DISABLED, command=self._on_close)
        label = _('Consolidate')
        icon  = Icons.load('next')
        menu.add_command(
                label=label, underline=0, accelerator='c',
                image=icon, compound=tk.LEFT,
                state=tk.DISABLED, command=self._on_close)
        label = _('Finish turn')
        icon  = Icons.load('stop')
        menu.add_command(
                label=label, underline=0, accelerator='f',
                image=icon, compound=tk.LEFT,
                state=tk.DISABLED, command=self._on_close)


    # Private methods: tk callbacks

    def _on_close(self):
        pass

    def _on_quit(self):
        """Request the controller to quit the application."""
        self.controller.do_quit()

    def _on_mnu_view_ratio(self):
        """Request the controller to toggle the aspect ratio."""
        self.controller.set_aspect_ratio(self._vars["ratio"].get())


    # -- Public methods: event bus handlers

    def on_new_game(self):
        log.info("Enabling in-game menus")
        to_be_enabled = {
            "game" : ["close"],
            "view" : ["ratio"],
        }
        for name, commands in to_be_enabled.items():
            menu = self._menus[name]

            for cmd in commands:
                index = self._indexes[name][cmd]
                log.debug(f'Enabling menu item {name}.{cmd} ({index})')
                menu.entryconfigure(index, state=tk.NORMAL)


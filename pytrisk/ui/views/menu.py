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

from pytrisk.locale   import _
from pytrisk.ui.utils import Icons

class MenuView(tk.Menu):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent)

        self.controller = controller

        # Menu: game
        menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label=_('Game'), underline=0, menu=menu)
        label = _('Close')
        icon  = Icons.load('close')
        menu.add_command(
                label=label, underline=0, accelerator='Ctrl+W',
                image=icon, compound=tk.LEFT,
                state=tk.DISABLED, command=self._on_close)
        menu.add_separator()
        icon  = Icons.load('quit')
        menu.add_command(
                label=_('Quit'), underline=0, accelerator='Ctrl+Q',
                image=icon, compound=tk.LEFT,
                command=self._on_quit)

        # Menu: actions
        menu = tk.Menu(self, tearoff=False)
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


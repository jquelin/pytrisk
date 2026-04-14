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
import tkinter.font as tkfont
import tkinter.ttk  as ttk
from TkToolTip import ToolTip

from pytrisk.locale   import _
from pytrisk.ui.utils import Icons

class ToolbarView(tk.Frame):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent)

        self.controller = controller
        iconsize = 16

        icon = Icons.load('quit', iconsize)
        but = tk.Button(self, image=icon, command=self.do_nothing)
        but.pack(side=tk.LEFT)
        tooltip = ToolTip(but, msg=_('Quit'))

        icon = Icons.load('close', iconsize)
        but = tk.Button(self, image=icon, state=tk.DISABLED,
                        command=self.do_nothing)
        but.pack(side=tk.LEFT)
        tooltip = ToolTip(but, msg=_('Close'))

        sep = ttk.Separator(self, orient=tk.VERTICAL)
        sep.pack(side=tk.LEFT, fill=tk.Y, padx=4, pady=4)

        font_bold = tkfont.Font(font='TkDefaultFont')
        font_bold.config(weight='bold')
        lab = tk.Label(self, text=_('Game state:'), font=font_bold)
        lab.pack(side=tk.LEFT)

        lab = tk.Label(self, text=_('place armies'), state=tk.DISABLED)
        lab.pack(side=tk.LEFT)

        icon = Icons.load('undo', iconsize)
        but = tk.Button(self, image=icon, state=tk.DISABLED,
                        command=self.do_nothing)
        but.pack(side=tk.LEFT)
        tooltip = ToolTip(but, msg=_('undo all'))

        icon = Icons.load('next', iconsize)
        but = tk.Button(self, image=icon, state=tk.DISABLED,
                        command=self.do_nothing)
        but.pack(side=tk.LEFT)
        tooltip = ToolTip(but, msg=_('ready for attack'))

        lab = tk.Label(self, text=_('attack'), state=tk.DISABLED)
        lab.pack(side=tk.LEFT)

        icon = Icons.load('redo', iconsize)
        but = tk.Button(self, image=icon, state=tk.DISABLED,
                        command=self.do_nothing)
        but.pack(side=tk.LEFT)
        tooltip = ToolTip(but, msg=_('attack again'))

        icon = Icons.load('next', iconsize)
        but = tk.Button(self, image=icon, state=tk.DISABLED,
                        command=self.do_nothing)
        but.pack(side=tk.LEFT)
        tooltip = ToolTip(but, msg=_('consolidate'))

        lab = tk.Label(self, text=_('move armies'), state=tk.DISABLED)
        lab.pack(side=tk.LEFT)

        icon = Icons.load('stop', iconsize)
        but = tk.Button(self, image=icon, state=tk.DISABLED,
                        command=self.do_nothing)
        but.pack(side=tk.LEFT)
        tooltip = ToolTip(but, msg=_('turn finished'))




    def do_nothing(self):
        pass

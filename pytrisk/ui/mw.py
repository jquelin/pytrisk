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

from pytrisk import config  # should go first

from pytrisk.locale import _
from ..logger import log
import pytrisk.data
from pytrisk.ui.tkhelper import Action

from pathlib import Path
import PIL.Image
import PIL.ImageTk
import tkinter as tk
from tkinter import *
from tkinter import ttk
import types

from pytrisk.constants import appinfo
from pytrisk.ui.utils         import Icons
from pytrisk.ui.views.menu    import MenuView
from pytrisk.ui.views.toolbar import ToolbarView


class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        # GUI creation
        log.info('creating main window')
        self.title(appinfo.title)
        self.iconphoto(True, Icons.load(appinfo.name, 32))
        self._create_views()

        self._build_startup_frame()
        # Add some bindings
        self.protocol('WM_DELETE_WINDOW', self._on_quit)
        self.bind('<Control-q>', self._on_quit)


    # -- gui construction

    def _create_views(self):
        """Create all views"""

        menu = MenuView(self, None, None)
        self.config(menu=menu)

        toolbar = ToolbarView(self, None, None)
        toolbar.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5)


    def _build_startup_frame(self):
        frame = Frame(self)
        frame.pack(side=TOP, expand=True, fill=BOTH)

        f = Frame(frame)
        f.pack(side=LEFT, expand=True, fill=Y)

        lab = Label(f, text=_('Map'))
        lab.pack(side=TOP)
        lb_maps = Listbox(f)
        lb_maps.pack(side=TOP, expand=True, fill=Y)

        maps = sorted(pytrisk.data.all_maps(), key=lambda x: x.title)
        for m in maps:
            lb_maps.insert(END, m.title)

        f_players = Frame(frame)
        f_players.pack(side=LEFT, expand=True, fill=BOTH)
        lab = Label(f_players, text=_('Players'))
        lab.pack(side=TOP)
        f = Frame(f_players)
        f.pack(side=TOP, fill=X)
        lab = Label(f, text=_('Number of players'))
        lab.pack(side=LEFT)
        scale = Scale(f, orient=HORIZONTAL, from_=2, to=10)
        scale.set(3)
        scale.pack(side=LEFT, fill=X)



    # -- gui callbacks

    def _on_quit(self, event=None):
        """Signal the controller we want to quit the application."""
        log.info('quitting')
        self.destroy()


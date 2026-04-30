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
from typing import Literal

from pytrisk.locale    import _
from pytrisk.logger    import log

Anchor = Literal['nw','n','ne','w','center','e','sw','s','se']


@dataclass
class Column:
    attr: str
    ctype: type = str


class StartupMapsView(tk.LabelFrame):
    """View to select the map.

    It shows a list of existing maps with some information, and allows the user
    to select one.

    When a map is selected, it signals the controller.
    """

    def __init__(self, parent, controller, event_bus):
        super().__init__(parent, text=_(' Map '), labelanchor=tk.N)

       # Subscribe to events & store the controller for later use.
        event_bus.subscribe(self)
        self.controller = controller

        # Prepare the treeview columns.
        self._map_columns = {
            "id"       : Column("id", str),
            "Name"     : Column("name", str),
            "Category" : Column("category", str),
            "#C"       : Column("nb_continents", int),
            "#c"       : Column("nb_countries", int),
        }

        # Prepare the treeview data.
        maps = self.controller.get_maps()
        self._maps = sorted(maps, key=lambda x: x.id)

        # Prepare the treeview headers, longest strings and alignments.
        font = tkfont.nametofont('TkHeadingFont')
        headers = list(self._map_columns.keys())
        longest = [
            font.measure(max([m.id for m in maps], key=len)) + 10,
            font.measure(max([m.name for m in maps], key=len)) + 10,
            font.measure(max([m.category for m in maps], key=len)) + 10,
            font.measure('XXX') + 10, # nb continents is a number
            font.measure('XXX') + 10  # nb countries is a number
        ]


        aligns: list[Anchor] = [tk.W, tk.W, tk.W, tk.CENTER, tk.CENTER]

        # Create the treeview to show the maps.
        tv = ttk.Treeview(self, columns=headers, height=20, show='headings',
                          selectmode=tk.BROWSE)
        self.tv = tv
        tv.pack(side=tk.LEFT, fill=tk.Y)
        tv.bind('<<TreeviewSelect>>', self._on_tv_map_selection)
        tv.bind('<Button-1>', self._on_tv_map_click)
        tv.tag_configure("odd", background='#DDDDDD')

        # Adjust the column's width to the header string
        for col, longest, anchor in zip(headers, longest, aligns):
            tv.heading(col, text=col, command=lambda c=col:
                       self._on_tv_map_sort(c, False))
            tv.column(col, width=longest, anchor=anchor) # type: ignore

        # Add a vertical scrollbar to the treeview.
        vsb = ttk.Scrollbar(self, orient="vertical", command=tv.yview)
        vsb.pack(side=tk.LEFT, fill=tk.Y)
        tv.configure(yscrollcommand=vsb.set)

        # Fill the treeview with the data.
        self._reload_treeview()


    # -- Private methods

    def _reload_treeview(self):
        """Reload the treeview with the data."""
        tv = self.tv
        tv.delete(*tv.get_children())

        for i, m in enumerate(self._maps):
            tags = [] if i % 2 == 0 else ['odd']
            tv.insert(
                '', tk.END, tags=(tags), iid=m.id,
                values=tuple(getattr(m, c.attr) for c in self._map_columns.values()),
            )


    # -- Event handlers

    def _on_tv_map_click(self, ev):
        """Event handler for treeview click.

        It is only used to prevent column resizing when the user clicks on the
        separator between columns, which would be annoying since the columns
        are automatically sized to fit their content, and the user doesn't need
        to resize them.
        """
        # prevent column resizing
        if self.tv.identify_region(ev.x, ev.y) == "separator":
             return "break"


    def _on_tv_map_selection(self, event):
        pass

    def _on_tv_map_sort(self, col: str, descending: bool):
        """Event handler for treeview column sorting. Sort the map list by the
        selected column. Then update the treeview so that heading click will
        sort in the opposite direction.

        Args:
            col (str): column to sort
            descending (bool): sort direction
        """
        log.info(f'Sorting map list by {col} {"descending" if descending else "ascending"}')

        # Get selected item
        tv = self.tv
        selected = tv.selection()
        curitem  = selected[0] if selected else None

        # Sort the map list
        col_def = self._map_columns[col]
        self._maps.sort(key=lambda x: getattr(x, col_def.attr), reverse=descending)
        self._reload_treeview()

        # Toggle sort
        tv.heading(col, command=lambda col=col: self._on_tv_map_sort(col, not descending))

        # Restore selection
        if curitem:
            tv.selection_set(curitem)
            tv.focus(curitem)
            tv.see(curitem)

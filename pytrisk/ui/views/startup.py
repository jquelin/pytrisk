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
import tkinter.font as tkfont

from pytrisk.locale    import _
from pytrisk.logger    import log


class StartupView(tk.Frame):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent)

       # Subscribe to events & store the controller for later use.
        event_bus.subscribe(self)
        self.controller = controller

        # Prepare the treeview data.
        maps = controller.get_maps()
        self.maps = sorted(maps, key=lambda x: x.id)
        font = tkfont.nametofont('TkHeadingFont')
        headers = ['Name', 'Description', '#C', '#c']
        longest = [
            font.measure(max([m.id for m in maps], key=len)) + 10,
            font.measure(max([m.name for m in maps], key=len)) + 10,
            font.measure('XXX') + 10,
            font.measure('XXX') + 10
        ]

        # Prepare the treeview headers, longest strings and alignments.
        aligns  = [tk.W, tk.W, tk.CENTER, tk.CENTER]

        # Create the treeview to show the maps.
        tv = ttk.Treeview(self, columns=headers, height=20, show='headings',
                          selectmode=tk.BROWSE)
        self.tv = tv
        tv.pack(side=tk.LEFT, fill=tk.Y)
        tv.bind('<<TreeviewSelect>>', self._on_tv_map_selection)
        tv.bind('<Button-1>', self._on_tv_map_click)

        tv.tag_configure("odd", background='#DDDDDD')

        for col, longest, anchor in zip(headers, longest, aligns):
            tv.heading(col, text=col, command=lambda c=col:
                       self._on_tv_map_sort(c, False))
            # adjust the column's width to the header string
            tv.column(col, width=longest, anchor=anchor)

        # Add a vertical scrollbar to the treeview.
        vsb = ttk.Scrollbar(self, orient="vertical", command=tv.yview)
        vsb.pack(side=tk.LEFT, fill=tk.Y)
        tv.configure(yscrollcommand=vsb.set)

        # Fill the treeview with the data.
        self._reload_treeview()


    def _reload_treeview(self):
        """Reload the treeview with the data."""
        tv = self.tv
        tv.delete(*tv.get_children())

        for i, d in enumerate(self.maps):
            tags = [] if i % 2 == 0 else ['odd']
            tv.insert('', tk.END, tags=(tags),
                        iid=d.id,
                        values=[d.id, d.name, d.nb_continents, d.nb_countries])

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

        attribute = {
            'Name': 'id',
            'Description': 'name',
            '#C': 'nb_continents',
            '#c': 'nb_countries'
        }

        # Sort
        self.maps.sort(
            key=lambda m: getattr(m, attribute[col]),
            reverse=descending
        )
        self._reload_treeview()

        # Toggle sort
        tv.heading(col, command=lambda col=col: self._on_tv_map_sort(col, not descending))

        # Restore selection
        if curitem:
            tv.selection_set(curitem)
            tv.focus(curitem)
            tv.see(curitem)

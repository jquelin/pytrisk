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

class StatusbarView(tk.Frame):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent)

        # Sunken inner frame to hold the widgets
        f = tk.Frame(self, relief=tk.SUNKEN, borderwidth=1)
        f.pack(side=tk.TOP, fill=tk.X, expand=True)

        # Label to display status
        statuslab = tk.Label(f, anchor=tk.W)
        statuslab.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1, pady=1)

        # Label to display country pointed by mouse
        countrylab= tk.Label(f, anchor=tk.E)
        countrylab.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=1, pady=1)



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

class Heading(tk.Frame):
    """A heading widget."""

    def __init__(self, parent, text):
        super().__init__(parent)

        # Create the label
        lab = tk.Label(self, text=text)
        lab = tk.Label(self, text=text,
                       bg='black', fg='white',
                       font=('TkDefaultFont', 14, 'bold'))
        lab.pack(side=tk.TOP, fill=tk.X, padx=20, pady=20)

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

from pytrisk.locale  import _
from pytrisk.logging import log

import csv
from pathlib import Path

maps_dir = Path(Path(__file__).parent, 'maps')

class Map():
    def __init__(self, name, title, author):
        self.name   = name
        self.title  = title
        self.author = author

def load_maps():
    maps = {}
    # first, open
    with open(Path(maps_dir, 'list.csv'), newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  # skip the headers
        for row in csvreader:
            name, title, author = row
            if title[0:2] == '_(':
                title = eval(title)
            maps[name] = Map(name, title, author)
        return maps


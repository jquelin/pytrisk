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
import yaml

maps_dir = Path(Path(__file__).parent, 'maps')

class Map():
    def __init__(self, name):
        self.name   = name
        self.path   = Path(maps_dir, name)
        self._load()

    def _load(self):
        self._load_infos()

    def _load_infos(self):
        # first, open yaml information file
        yfile = Path(self.path, 'info.yaml')
        with yfile.open() as ystream:
            try:
                info = yaml.safe_load(ystream)
            except yaml.YAMLError as e:
                log.error('error loading {yfile.as_posix()}: {e}')
        self.title = info['title']
        self.author = info['author']



def all_maps():
    subdirs = [d for d in maps_dir.glob('*')]
    log.debug(f'found {len(subdirs)} map subdirs in {maps_dir.as_posix()}')
    maps = {}
    for subdir in subdirs:
        mapname      = subdir.name
        maps[mapname] = Map(mapname)
    return maps

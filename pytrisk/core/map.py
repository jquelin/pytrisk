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

import tomllib

from pytrisk.logger import log


class Map:
    '''Map representation.'''

    def __init__(self, dirname):
        log.info(f'Creating map from {dirname}')

        # Map files
        self.dir = dirname
        self.file = dirname / 'map.toml'
        self.background = dirname / 'background.png'
        self.overlay    = dirname / 'overlay.png'

        # Load map file
        log.debug(f'Loading map file {self.file}')
        self._data = tomllib.loads(self.file.read_text())

        # Extract general information
        self.id   = dirname.name
        self.info = self._data['info']
        self.name = self.info['name']

        self.nb_continents = len(self._data['continents'])
        self.nb_countries  = len(self._data['countries'])

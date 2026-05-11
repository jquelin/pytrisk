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

import json

from pytrisk.domain.continent import Continent
from pytrisk.domain.country   import Country
from pytrisk.logger import log


class Map:
    '''Map representation.'''

    def __init__(self, dirname):
        log.info(f'Creating map {dirname.name}')

        # Map files
        self.dir = dirname
        self.file = dirname / 'map.json'
        self.background = dirname / 'background.png'
        self.overlay    = dirname / 'overlay.png'

        # Read map file
        log.debug(f'Reading map file {self.file}')
        self._data = json.loads(self.file.read_text())

        # Extract general information
        self.id       = dirname.name
        self.name     = self._data['name']
        self.category = self._data['category']

        self.nb_continents = len(self._data['continents'])
        self.nb_countries  = len(self._data['countries'])
        log.debug(f'Map {self.id}: {self.category} "{self.name}" '
                 f'({self.nb_continents} continents, {self.nb_countries} countries)')


    # -- Public method

    def load(self):
        """Load the map and instantiate the continents and countries. Before
        this, the map is a just the data read from the map definition."""
        log.info(f'Loading map {self.id}')
        self.continents = [Continent(self, c) for c in self._data['continents']]
        self.countries  = [Country(self, c) for c in self._data['countries']]


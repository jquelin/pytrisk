# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

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

    @property
    def continents(self):
        """Return the list of continents."""
        return list(self._continents.values())

    @property
    def countries(self):
        """Return the list of continents."""
        return list(self._countries.values())

    def load(self):
        """Load the map and instantiate the continents and countries. Before
        this, the map is a just the data read from the map definition."""
        log.info(f'Loading map {self.id}')
        self._continents = {c["id"] : Continent(self, c) for c in self._data['continents']}
        self._countries  = {c["id"] : Country(self, c) for c in self._data['countries']}


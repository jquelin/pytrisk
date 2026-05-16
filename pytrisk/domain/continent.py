# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import weakref

from pytrisk.logger import log

class Continent:
    '''Continent representation.'''

    def __init__(self, map, c: dict):
        log.info(f'Creating continent {c["name"]}')

        # Record attributes
        self._map  = weakref.ref(map)   # weak reference to map
        self.id    = c['id']            # Continent id
        self.name  = c['name']          # Continent name
        self.color = c['color']         # Continent color
        self.bonus = c['bonus']         # Continent bonus

        # Fix colors if needed
        self._fix_colors()

    @property
    def countries(self):
        all_countries = self.map.countries
        return [c for c in all_countries if c.continent_id == self.id]

    @property
    def map(self):
        return self._map()

    # -- Private methods

    def _fix_colors(self):
        """Fix colors if needed."""
        real_colors = [
            "#E53935",  # red
            "#1E88E5",  # blue
            "#43A047",  # green
            "#FB8C00",  # orange
            "#8E24AA",  # purple
            "#00ACC1",  # cyan
            "#D81B60",  # pink
            "#FDD835",  # yellow
            "#6D4C41",  # brown
            "#7CB342",  # lime
            "#3949AB",  # indigo
            "#00897B",  # teal
            "#C2185B",  # magenta
            "#FFB300",  # amber
            "#546E7A",  # blue grey
            "#26A69A",  # mint
            "#AD1457",  # dark pink
            "#9E9D24",  # olive
            "#039BE5",  # sky blue
            "#FF7043",  # coral
            "#5E35B1",  # deep purple
            "#00838F",  # dark cyan
            "#C0CA33",  # yellow green
            "#F4511E",  # deep orange
        ]
        if self.color.startswith('col'):
            log.warning(f'Unknown continent color: {self.color}')
            self.color = real_colors[self.id - 1]


    # -- Public methods



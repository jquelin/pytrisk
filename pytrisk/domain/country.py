# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import weakref

from pytrisk.logger import log


class Country:
    '''Continent representation.'''

    def __init__(self, map, c: dict):
        log.info(f'Creating country {c["name"]}')

        # Record attributes
        self._map         = weakref.ref(map)   # weak reference to map
        self.id           = c['id']            # Country id
        self.x            = c['x']             # Country x
        self.y            = c['y']             # Country y
        self.continent_id = c['continent']     # Id of continent
        self.name         = c['name']          # Country name
        self._connections = c['connections']   # List of connections


    # -- Private methods


    # -- Public methods


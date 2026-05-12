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
        self.map   = weakref.ref(map)   # weak reference to map
        self.id    = c['id']            # Continent id
        self.name  = c['name']          # Continent name
        self.color = c['color']         # Continent color
        self.bonus = c['bonus']         # Continent bonus


    # -- Private methods
    # -- Public methods


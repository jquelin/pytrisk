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


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

import time

from pytrisk.constants  import appinfo
from pytrisk.domain.map import Map
from pytrisk.logger     import log


class GameContext:
    """ Application class, main entry point for the controller. """

    def __init__(self):
        # initialize data and game
        self._create_maps()

    # -- Private maps

    def _create_maps(self):
        '''Create maps from map definition. It is not yet fully loaded.
        '''
        log.info('Creating maps')
        start = time.perf_counter()
        mapdir = appinfo.dirs.share / 'maps'
        self.maps = {}
        for f in mapdir.iterdir():
            if f.is_dir():
                self.maps[f.name] = Map(f)

        end = time.perf_counter()
        log.info(f'Created {len(self.maps)} maps in {end - start:.2f} seconds')

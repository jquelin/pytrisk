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

import PIL.Image
import PIL.ImageTk

from pytrisk.constants import appinfo
from pytrisk.logger    import log


class Icons:
    _cache = {}

    @classmethod
    def load(cls, name, size=24):
        """Load an icon and return it ready to be used by tk"""
        size = str(size)

        # check if icon is already loaded
        cached = name + '_' + size
        if cached in cls._cache:
            return cls._cache[cached]

        # icon not loaded, first compute path
        path = appinfo.dirs.share / 'icons' / size / f'{name}.png'
        path = path.absolute().as_posix()
        log.debug(f'loading icon {path}')

        # load image and convert to RGBA if needed
        img = PIL.Image.open(path)
        if img.mode != 'RGBA':
            img = img.convert(mode="RGBA")

        # create the icon ready to be used by tk, store it and return it
        icon = PIL.ImageTk.PhotoImage(img)
        cls._cache[cached] = icon
        return icon



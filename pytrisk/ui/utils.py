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

from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage
from pathlib import Path

from pytrisk.constants import appinfo
from pytrisk.logger    import log


class Icons:
    _cache: dict[str, PhotoImage] = {}

    @classmethod
    def load(cls, name: str) -> PhotoImage:
        """Load an icon and return it ready to be used by tk."""

        # cache hit
        cached = cls._cache.get(name)
        if cached is not None:
            return cached

        # build path
        path: Path = appinfo.dirs.share / "icons" / f"{name}.png"
        filename = path.resolve().as_posix()
        log.debug(f"loading icon {filename}")

        # load image via PIL
        img = Image.open(filename)
        if img.mode != "RGBA":
            img = img.convert("RGBA")

        # convert to Tk-compatible image
        icon = ImageTk.PhotoImage(img)

        # store in cache
        cls._cache[name] = icon

        return icon


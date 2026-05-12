# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

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


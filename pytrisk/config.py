# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import json
from pathlib import Path

from pytrisk.constants import appinfo
from pytrisk.logger    import log


class ConfigFile:
    def __init__(self, path):
        self.path = path
        self.data = self._load()

    def _load(self):
        """Load configuration from disk."""
        if self.path.exists():
            return json.loads(self.path.read_text())
        return {}

    # -- Public methods

    def save(self):
        """Save configuration to disk. """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=4)


class Config:
    """Main configuration manager.

        Args:
            default_path (str | Path): Path to default file.
            user_path (str | Path): Path to user file.
    """

    def __init__(self, default_path, user_path):
        """
        """

        self._default = ConfigFile(default_path)
        self._user    = ConfigFile(user_path)


    # -- Public methods

    def get(self, key):
        if key in self._user.data:
            return self._user.data[key]
        return self._default.data[key]

    def set(self, key, value):
        default_value = self._default.data[key]

        if value == default_value:
            self._user.data.pop(key, None)
        else:
            self._user.data[key] = value
        self._user.save()


config = Config(
    default_path = appinfo.dirs.share / "config" / "default.json",
    user_path    = appinfo.dirs.local / "user.json",
)

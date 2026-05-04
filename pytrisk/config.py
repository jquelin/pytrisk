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

import tomllib
import tomli_w
from pathlib import Path
from collections.abc import Mapping

from pytrisk.constants import appinfo
from pytrisk.logger    import log

class ConfigStore:
    """
    Storage layer for configuration data.

    Wraps a nested dictionary and provides utilities for:
    - deep get
    - deep set
    - deep delete with cleanup

    This class is unaware of any default/user logic.
    """

    def __init__(self, data=None):
        """
        Args:
            data (dict | None): Initial configuration data.
        """
        self.data = data or {}


    # -- Public methods

    def get(self, path):
        """
        Retrieve a value from the nested dictionary.

        Args:
            path (list[str]): Path to the value.

        Returns:
            Any: Retrieved value.

        Raises:
            KeyError: If the path does not exist.
        """
        node = self.data
        for key in path:
            if not isinstance(node, dict) or key not in node:
                raise KeyError(path)
            node = node[key]
        return node

    def set(self, path, value):
        """
        Set a value in the nested dictionary.

        Intermediate dictionaries are created if needed.

        Args:
            path (list[str]): Path to the value.
            value (Any): Value to set.
        """
        node = self.data
        for key in path[:-1]:
            node = node.setdefault(key, {})
        node[path[-1]] = value

    def delete(self, path):
        """
        Delete a value from the nested dictionary.

        Also removes empty parent dictionaries recursively.

        Args:
            path (list[str]): Path to delete.
        """
        node = self.data
        parents = []

        for key in path[:-1]:
            if key not in node:
                return
            parents.append((node, key))
            node = node[key]

        node.pop(path[-1], None)

        # Cleanup empty dictionaries
        for parent, key in reversed(parents):
            if not parent[key]:
                parent.pop(key)
            else:
                break


class ConfigView:
    """
    Proxy object representing a node in the configuration tree.

    Provides attribute-style access to nested configuration values,
    e.g. config.foo.bar.

    Delegates all operations to the root Config instance.
    """

    def __init__(self, config, path):
        """
        Args:
            config (Config): Root configuration object.
            path (list[str]): Path to this node.
        """
        self._config = config
        self._path = path

    def __getattr__(self, name):
        """
        Retrieve a child value or node.

        Args:
            name (str): Attribute name.

        Returns:
            Any | ConfigView: Returns a new ConfigView if the value is a mapping,
                              otherwise returns the value.
        """
        path = self._path + [name]
        try:
            value = self._config._get(path)
        except KeyError:
            log.warning(f'unknown config path: {".".join(path)}, returning None')
            raise

        if isinstance(value, Mapping):
            return ConfigView(self._config, path)

        return value

    def __getitem__(self, key):
        path = self._path + [key]
        value = self._config._get(path)

        if isinstance(value, Mapping):
            return ConfigView(self._config, path)

        return value

    def __setattr__(self, name, value):
        """
        Set a value at the given path.

        Behavior:
        - If value equals default → remove from user config
        - Otherwise → store in user config

        Args:
            name (str): Attribute name.
            value (Any): Value to set.
        """
        if name.startswith("_"):
            return super().__setattr__(name, value)

        path = self._path + [name]
        self._config._set(path, value)


class Config:
    """
    Main configuration manager.

    Handles:
    - layered configuration (default + user)
    - dynamic resolution (user overrides default)
    - attribute-style access via ConfigView
    - persistence of user overrides

    The user configuration only stores values different from defaults.
    """

    def __init__(self, default_path, user_path):
        """
        Args:
            default_path (str | Path): Path to default TOML file.
            user_path (str | Path): Path to user TOML file.
        """
        self._default_path = Path(default_path)
        self._user_path = Path(user_path)

        self._default = ConfigStore(self._load(self._default_path))
        self._user = ConfigStore(self._load(self._user_path))


    # -- Private methods: File handling

    def _load(self, path):
        """
        Load a TOML file.

        Args:
            path (Path): File path.

        Returns:
            dict: Parsed data or empty dict if file does not exist.
        """
        if path.exists():
            with open(path, "rb") as f:
                return tomllib.load(f)
        return {}


    def _save_user(self):
        """
        Save user configuration to disk.
        """
        self._user_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._user_path, "wb") as f:
            tomli_w.dump(self._user.data, f)

    # -------------------------
    # Core logic
    # -------------------------

    def _get(self, path):
        """
        Retrieve a value with fallback logic.

        Resolution order:
        1. user config
        2. default config

        Args:
            path (list[str]): Path to value.

        Returns:
            Any: Resolved value.

        Raises:
            KeyError: If not found in either config.
        """
        try:
            return self._user.get(path)
        except KeyError:
            return self._default.get(path)

    def _get_default(self, path):
        """
        Retrieve a value from default config only.

        Args:
            path (list[str]): Path to value.

        Returns:
            Any: Default value or None if missing.
        """
        try:
            return self._default.get(path)
        except KeyError:
            return None

    def _set(self, path, value):
        """
        Set a configuration value.

        Behavior:
        - If value equals default → remove from user config
        - Otherwise → store in user config

        Args:
            path (list[str]): Path to value.
            value (Any): Value to set.
        """
        default_value = self._get_default(path)

        if value == default_value:
            self._user.delete(path)
        else:
            self._user.set(path, value)

        self._save_user()

    # -------------------------
    # Public API
    # -------------------------

    def __getattr__(self, name):
        """
        Retrieve a top-level configuration value or node.

        Args:
            name (str): Attribute name.

        Returns:
            Any | ConfigView
        """
        value = self._get([name])

        if isinstance(value, Mapping):
            return ConfigView(self, [name])

        return value

config = Config(
    default_path = appinfo.dirs.share / "config" / "default.toml",
    user_path    = appinfo.dirs.local / "user.toml",
)

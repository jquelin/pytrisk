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

from pathlib import Path
import appdirs
import contextlib

# create config directory if needed
_config_dir = Path(appdirs.user_config_dir('pytrisk'))
_config_dir.mkdir(parents=True, exist_ok=True)

# read & parse config file
_config_file = Path(_config_dir, 'pytrisk.cfg')
_config = {}

with contextlib.suppress(FileNotFoundError):
    with _config_file.open() as file:
        for line in file.readlines():
            line = line.rstrip()
            (key, value) = line.split('=', 1)
            _config[key] = value

def get(key, default=None):
    if key in _config:
        return _config[key]
    return default

def set(key, value):
    # store new value
    _config[key] = value
    # then write file for persistence
    with _config_file.open('w') as file:
        for key, value in _config.items():
            line = f'{key}={value}\n'
            print(line)
            file.write(line)

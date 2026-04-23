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

import appdirs
from pathlib import Path


class appinfo:
    name  = "pytrisk"
    title = 'pytrisk'

# -- Application directories

class dirs:
    local = Path(appdirs.user_config_dir(appinfo.name)).absolute()
    cache = Path(appdirs.user_cache_dir(appinfo.name)).absolute()
    logs  = Path(appdirs.user_log_dir(appinfo.name)).absolute()
    share = Path(__file__).parent / "share"
appinfo.dirs = dirs

appinfo.dirs.local.mkdir(parents=True, exist_ok=True)
appinfo.dirs.cache.mkdir(parents=True, exist_ok=True)
appinfo.dirs.logs.mkdir(parents=True, exist_ok=True)

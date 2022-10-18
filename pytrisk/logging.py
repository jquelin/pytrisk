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

import logging
import colorlog


colors = colorlog.default_log_colors
colors['DEBUG'] = 'blue'
colors['INFO']  = 'white'
formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    log_colors=colors
)
handler = colorlog.StreamHandler()
handler.setFormatter(formatter)
log = colorlog.getLogger('pytrisk')
log.addHandler(handler)
log.setLevel(logging.DEBUG)


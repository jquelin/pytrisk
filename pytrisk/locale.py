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

import gettext
import os
BASE_DIR = os.path.dirname(__file__)
LOCALE_DIR = os.path.join(BASE_DIR, 'locale')

gettext.bindtextdomain('pytrisk', LOCALE_DIR)
gettext.textdomain('pytrisk')

_ = gettext.gettext

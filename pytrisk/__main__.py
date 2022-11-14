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

from pytrisk import config
from pytrisk.locale import _
from pytrisk.logging import log
from pytrisk import gui
from pytrisk import maps

print( _('this is a test'))
m = maps.all_maps()
print(m['risk'])


def run():
    # make sure we can run the gui from dev
    import sys
    sys.path.append('.')
    gui.run()



if __name__ == '__main__':
    run()

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


import argparse

from pytrisk.constants           import appinfo
from pytrisk.domain.game_context import GameContext
from pytrisk.controller          import Controller
from pytrisk.events              import EventBus
from pytrisk.logger              import log
import pytrisk.ui.mw

def run():
    parser = argparse.ArgumentParser(
        prog=appinfo.name,
        description='Risk game',
    )
    parser.add_argument('-v', '--verbose', action='count', default=0,
                            help='Increase verbosity level')
    parser.add_argument('-q', '--quiet', action='count', default=0,
                            help='Decrease verbosity level')
    args = parser.parse_args()

    # Adjust logging level based on verbosity flags
    for _ in range(args.quiet):
        log.decrease_verbosity()
    for _ in range(args.verbose):
        log.increase_verbosity()

    # create the game context, event bus and controller
    context    = GameContext()
    event_bus  = EventBus()
    controller = Controller(context, event_bus)

    # create the gui and start the main loop
    ui = pytrisk.ui.mw.MainWindow(controller, event_bus)
    ui.mainloop()

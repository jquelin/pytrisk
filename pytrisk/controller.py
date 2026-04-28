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

from pytrisk.logger import log
from pytrisk.events import Events


class Controller:
    def __init__(self, app, event_bus):
        # Store the app and event bus
        self.app = app
        self.event_bus = event_bus

    # -- Current state retrieval

    # -- Data retrieval

    def get_player_colors(self):
        """Return the list of available player colors."""
        return [
            '#333333',  # grey20
            '#FF2052',  # awesome
            '#01A368',  # green
            '#0066FF',  # blue
            '#9E5B40',  # sepia
            '#A9B2C3',  # cadet blue
            '#BB3385',  # red violet
            '#FF681F',  # orange
            '#DCB63B',  # ~ dirty yellow
            '#00CCCC',  # robin's egg blue
            #'#1560BD',  # denim
            #'#33CC99',  # shamrock
            #'#FF9966',  # atomic tangerine
            #'#00755E',  # tropical rain forest
            #'#A50B5E',  # jazzberry jam
            #'#A3E3ED',  # blizzard blue
        ]


    def get_maps(self):
        """Return the list of available maps."""
        return self.app.maps.values()

    # -- Action handlers

    def do_quit(self):
        """Quit the application."""
        log.info('Request to quit')
        self.event_bus.emit(Events.action_quit)


    # -- Preferences retrieval / setting

    # -- Private methods


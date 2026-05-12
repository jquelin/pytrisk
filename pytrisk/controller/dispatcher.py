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

from pytrisk.controller.game     import GameController
from pytrisk.controller.main     import MainController
from pytrisk.controller.startup  import StartupController
from pytrisk.logger import log


class Controller:
    """
    Controller that dispatches events to subcontrollers. It is totally
    transparent for the rest of the application.
    """
    def __init__(self, context, event_bus):
        # subcontrollers
        self._controllers = [
            MainController(self, context, event_bus),
            StartupController(self, context, event_bus),
            GameController(self, context, event_bus)
        ]

    def __getattr__(self, name):
        """Dispatch events to subcontrollers automatically."""
        for controller in self._controllers:
            if hasattr(controller, name):
                log.debug(f'Found method {name} in {controller.__class__.__name__}')
                return getattr(controller, name)

        raise AttributeError(name)


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


from enum import Enum

from pytrisk.logger import log

class Events(Enum):
    pass


class EventBus:
    """A simple event bus implementation to allow decoupled communication
    between different parts of the application. Components can subscribe to
    specific events and emit events with arbitrary arguments. This allows for a
    flexible and extensible architecture, where new features can be added
    without modifying existing code, and components can react to events without
    needing to know about each other."""

    def __init__(self):
        self.listeners = {}

    def subscribe(self, event, callback):
        """Subscribe a callback function to a specific event. The callback will
        be called with the arguments passed to the emit method when the event
        is emitted."""
        log.debug(f'Event subscribed: {event}')
        self.listeners.setdefault(event, []).append(callback)

    def emit(self, event, *args, **kwargs):
        """Emit an event with the given arguments. All callbacks subscribed to
        this event will be called with the provided arguments."""
        log.info(f'Event emitted: {event}')
        for cb in self.listeners.get(event, []):
            log.debug(f'calling callback: {cb}')
            cb(*args, **kwargs)

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


from enum import StrEnum, auto

from pytrisk.logger import log

class Events(StrEnum):
    action_quit          = auto()
    player_color_changed = auto()
    player_name_changed  = auto()
    status_clear         = auto()
    status_message       = auto()


class EventBus:
    """A simple event bus implementation to allow decoupled communication
    between different parts of the application. Components can subscribe to
    specific events and emit events with arbitrary arguments. This allows for a
    flexible and extensible architecture, where new features can be added
    without modifying existing code, and components can react to events without
    needing to know about each other."""

    def __init__(self):
        self.listeners = {}

    def subscribe(self, listener):
        """Subscribe an object. Its methods named on_<event> will be registered."""
        log.info(f'Subscribing {listener.__class__.__name__}')
        for event in Events:
            method_name = f'on_{event.name}'
            if hasattr(listener, method_name):
                cb = getattr(listener, method_name)
                log.debug(f'Auto-subscribed: {event} -> {listener.__class__.__name__}.{method_name}')
                self.listeners.setdefault(event, []).append(cb)


    def emit(self, event, *args, **kwargs):
        """Emit an event with the given arguments. All callbacks subscribed to
        this event will be called with the provided arguments."""
        log.info(f'Event emitted: {event}')
        for cb in self.listeners.get(event, []):
            log.debug(f'calling callback: {cb.__qualname__}')
            cb(*args, **kwargs)

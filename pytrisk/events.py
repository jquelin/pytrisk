# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.


from enum import StrEnum, auto
import weakref

from pytrisk.logger import log

class Events(StrEnum):
    action_quit          = auto()
    aspect_ratio_changed = auto()
    nb_players_changed   = auto()
    new_game             = auto()
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
                method = getattr(listener, method_name)
                wm = weakref.WeakMethod(method)
                log.debug(f'Auto-subscribed: {event} -> {listener.__class__.__name__}.{method_name}')
                self.listeners.setdefault(event, []).append(wm)


    def emit(self, event, *args, **kwargs):
        """Emit an event with the given arguments. All callbacks subscribed to
        this event will be called with the provided arguments."""
        log.info(f'Event emitted: {event}')

        # Call callbacks
        callbacks = self.listeners.get(event, [])
        alive = []
        nb_callbacks = len(callbacks)
        for idx, wm in enumerate(callbacks):
            cb = wm()
            if cb is not None:
                log.debug(f'callback {idx+1}/{nb_callbacks}: calling {cb.__qualname__}')
                cb(*args, **kwargs)
                alive.append(wm)
            else:
                log.debug(f'callback {idx+1}/{nb_callbacks}: dead (was {wm})')

        # Purge dead callbacks
        self.listeners[event] = alive

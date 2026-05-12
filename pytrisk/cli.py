# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import argparse
import signal

from pytrisk.constants             import appinfo
from pytrisk.domain.game_context   import GameContext
from pytrisk.controller.dispatcher import Controller
from pytrisk.events                import EventBus
from pytrisk.logger                import log
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

    # create the gui and start the main loop
    ui.mainloop()

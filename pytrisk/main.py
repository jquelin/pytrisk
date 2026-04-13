
import argparse

from pytrisk.constants import appinfo
from pytrisk.logger import log

#from .core.app import Application
#from .controller.controller import Controller
#from .ui.events import EventBus
#from pytrisk.gui.main import GraphicalUI
import pytrisk.gui.main

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

    # create the application, event bus and controller
#    app        = Application()
#    event_bus  = EventBus()
#    controller = Controller(app, event_bus)

    ui = pytrisk.gui.main.MainWindow()
    ui.mainloop()


if __name__ == '__main__':
    run()

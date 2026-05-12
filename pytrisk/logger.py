# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import colorlog
import logging
from termcolor import colored

from .constants import appinfo


class Logger:
    def __init__(self):
        # create our logger
        log = colorlog.getLogger(appinfo.name)
        log.setLevel(logging.DEBUG)
        self.log = log

        # attach some handlers
        self._create_console_handler()
        self._create_file_handler()


    # -- Private methods

    def _create_console_handler(self):
        """Create a console handler with color support."""

        # add the color console handler
        colors = colorlog.default_log_colors
        colors['DEBUG'] = 'blue'
        #colors['INFO']  = 'white'
        formatter = colorlog.ColoredFormatter(
            colored('s%(asctime)s ', 'dark_grey') +
            colored('[%(filename)s:%(lineno)d:%(funcName)s] ', 'yellow') +
            '%(log_color)s%(levelname)s%(reset)s '
            '%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors=colors
        )
        handler = colorlog.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(logging.WARNING)
        self.console_handler = handler
        self.log.addHandler(handler)


    def _create_file_handler(self):
        """Create a file handler for logging to a file."""

        formatter = logging.Formatter(
            '%(asctime)s '
            '[%(filename)s:%(lineno)d:%(funcName)s] '
            '%(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )

        logfile = appinfo.dirs.logs / 'debug.log'
        self.log.info(f'Logging to file {logfile}')
        self.file_handler = logging.FileHandler(logfile, mode='w')
        self.file_handler.setFormatter(formatter)
        self.file_handler.setLevel(logging.DEBUG)  # always DEBUG
        self.log.addHandler(self.file_handler)


    # -- Magic methods

    def __getattr__(self, name):
        """Delegate attribute access to the underlying logger."""
        return getattr(self.log, name)


    # -- Public methods

    def increase_verbosity(self):
        """Increase the verbosity level (lower the log level)."""

        current_level = self.console_handler.level
        if current_level > logging.DEBUG:
            new_level = current_level - 10
            self.console_handler.setLevel(new_level)
            self.log.debug(f'Increased verbosity to {logging.getLevelName(new_level)}')

    def decrease_verbosity(self):
        """Decrease the verbosity level (raise the log level)."""

        current_level = self.console_handler.level
        if current_level < logging.CRITICAL:
            new_level = current_level + 10
            self.console_handler.setLevel(new_level)
            self.log.debug(f'Decreased verbosity to {logging.getLevelName(new_level)}')

log = Logger()


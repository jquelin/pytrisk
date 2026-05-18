# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# _his file is part of pytrisk.

import random

from pytrisk.locale import _

class AINames:
    def __init__(self):
        self.names = [
            _('Napoleon Bonaparte'),   # France,   1769  - 1821
            _('Alexander the Great'),  # greece,   356BC - 323BC
            _('Julius Caesar'),        # Rome,     100BC - 44BC
            _('Attila'),               # Hun,      406   - 453
            _('Genghis Kahn'),         # Mongolia, 1162  - 1227
            _('Charlemagne'),          # France,   747   - 814
            _('Saladin'),              # Iraq,     1137  - 1193
            _('Otto von Bismarck'),    # Germany,  1815  - 1898
            _('Ramses II'),            # Egypt,    1303BC - 1213BC
            _('Sun _zu'),              # China,    645BC - 581BC
            _('Darth Vader'),          # Star Wars, 1980
            _('Sauron'),               # Lord of the Rings, 1954
            _('Palpatine'),            # Star Wars, 1977
            _('Magneto'),              # Marvel Comics, 1970
            _('Skynet'),               # Terminator, 1984
            _('HAL 9000'),             # 2001: A Space Odyssey, 1968
        ]

        # randomize the list
        random.shuffle(self.names)

    def get_name(self):
        return self.names.pop()


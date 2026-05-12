# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import gettext
from pathlib import Path

from pytrisk.constants import appinfo

# prepare l10n support
locale_dir = appinfo.dirs.share / 'locale'

gettext.bindtextdomain(appinfo.name, locale_dir)
gettext.textdomain(appinfo.name)

# exported function
_ = gettext.gettext

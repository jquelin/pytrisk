# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import appdirs
from dataclasses import dataclass
from importlib.metadata import version
from pathlib import Path


# -- Application directories

@dataclass(frozen=True)
class AppDirs:
    local : Path
    cache : Path
    logs  : Path
    share : Path

def _create_dirs(app_name: str) -> AppDirs:
    local = Path(appdirs.user_config_dir(app_name)).absolute()
    cache = Path(appdirs.user_cache_dir(app_name)).absolute()
    logs  = Path(appdirs.user_log_dir(app_name)).absolute()
    share = Path(__file__).parent / "share"

    local.mkdir(parents=True, exist_ok=True)
    cache.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)

    return AppDirs(
        local = local,
        cache = cache,
        logs  = logs,
        share = share,
    )


# -- Application metadata

@dataclass(frozen=True)
class AppInfo:
    name    : str
    title   : str
    dirs    : AppDirs
    version : str = version("pytrisk")



# -- Public API

appinfo = AppInfo(
    name  = "pytrisk",
    title = "pytrisk",
    dirs  = _create_dirs("pytrisk"),
)

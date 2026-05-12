# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.


from dataclasses import dataclass

@dataclass(frozen=True)
class GUISettings:
    wait_redraw   : int = 100  # ms
    wait_validate : int = 250  # ms

gui = GUISettings()

# --

@dataclass(frozen=True)
class PlayerSettings:
    max_count : int = 6
    colors    : tuple[str, ...] = (
            '#333333',  # grey20
            '#FF2052',  # awesome
            '#01A368',  # green
            '#0066FF',  # blue
            '#DCB63B',  # ~ dirty yellow
            '#9E5B40',  # sepia
            '#A9B2C3',  # cadet blue
            '#BB3385',  # red violet
            '#FF681F',  # orange
            '#00CCCC',  # robin's egg blue
            '#FFB347',  # pastel orange
            '#2E8B57',  # sea green
            '#4682B4',  # steel blue
            '#C71585',  # medium violet red
            '#708090',  # slate gray
            '#B22222',  # firebrick
            '#DAA520',  # goldenrod
            '#40E0D0',  # turquoise
            '#8A2BE2',  # blue violet
            '#CCCCCC',  # light gray
        )

players = PlayerSettings()


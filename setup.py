#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

PACKAGES = [
    'decider',
    'decider.features',
    'decider.links',
    'decider_footnote',
    'decider_footnote.features',
    'decider_footnote.rules',
    'decider_imgfig',
    'decider_imgfig.features',
    'fonts',
    'fonts.features',
]
ENTRY_POINTS = dict(console_scripts=[
    'decider = decider.cli:main',
    'decider_fonts = fonts.cli:main',
    'decider_footnote = decider_footnote.cli:main',
    'decider_imgfig = decider_imgfig.cli:main',
])

if __name__ == "__main__":
    utila.install(__file__)

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import iamraw

PATTERN = re.compile(
    r"""(
         ((?P<shortcut>[a-z]+)(?P<value>-{0,1}\d+))
         ?p(?P<page>-{0,1}\d+)                        # page can be negative
        )
     """,
    re.VERBOSE,
)

iamraw.Location.PATTERN = PATTERN

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo

import decider
import decider_footnote.path

ROOT = decider.ROOT

__version__ = decider.__version__

PROCESS = 'decider_footnote'

configo.cloud_lookup(PROCESS)

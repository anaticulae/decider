#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Decider judges different features based on previous feature extraction.

Currently `decider` supports:

    - titlepage validation

"""

import os

__version__ = '0.4.1'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# public API for further processing steps to gather correct file names and
# configuration.
# pylint:disable=wrong-import-position

PACKAGE = 'decider'
PROCESS = 'decider'

from decider.cli import DEVELOPER_LINT_OUTPUT  # isort:skip
from decider.cli import USER_LINT_OUTPUT  # isort:skip

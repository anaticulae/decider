# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from os.path import exists
from os.path import join

from decider import ROOT

TEST_DATA = join(ROOT, 'tests/data')
assert exists(TEST_DATA), TEST_DATA

RAWMAKER_RESULT = join(TEST_DATA, 'rawmaker')
assert exists(RAWMAKER_RESULT), RAWMAKER_RESULT

DECIDER_FONTS = join(TEST_DATA, 'decider_fonts')
assert exists(DECIDER_FONTS), DECIDER_FONTS

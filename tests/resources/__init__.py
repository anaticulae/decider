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

TEST_DATA = join(ROOT, 'tests/resources')
assert exists(TEST_DATA), TEST_DATA

TEST_CONFIG_DATA = join(ROOT, 'tests/config')

DECIDER_FONTS = join(TEST_CONFIG_DATA, 'decider_fonts')
assert exists(DECIDER_FONTS), DECIDER_FONTS

DOCU = join(TEST_DATA, 'docu')
DOCU_TWINE = join(DOCU, 'twine.pdf')

for item in [DOCU, DOCU_TWINE]:
    assert exists(item), str(item)

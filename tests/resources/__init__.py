# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import decider

RESOURCES = os.path.join(decider.ROOT, 'tests/resources')
assert os.path.exists(RESOURCES), RESOURCES

TEST_CONFIG_DATA = os.path.join(decider.ROOT, 'tests/config')

DECIDER_FONTS = os.path.join(TEST_CONFIG_DATA, 'decider_fonts')
assert os.path.exists(DECIDER_FONTS), DECIDER_FONTS

DOCU = os.path.join(RESOURCES, 'docu')
DOCU_TWINE = os.path.join(DOCU, 'twine.pdf')

for item in [DOCU, DOCU_TWINE]:
    assert os.path.exists(item), str(item)

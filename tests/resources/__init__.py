# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power

import decider

RESOURCES = os.path.join(decider.ROOT, 'tests/resources')
assert os.path.exists(RESOURCES), RESOURCES

GENERATED = os.path.join(RESOURCES, 'generated')

TEST_CONFIG_DATA = os.path.join(decider.ROOT, 'tests/config')

DECIDER_FONTS = os.path.join(TEST_CONFIG_DATA, 'decider_fonts')
assert os.path.exists(DECIDER_FONTS), DECIDER_FONTS

TODO = [
    (power.MASTER116_PDF, '0:50,90:115'),
    (power.MASTER098_PDF, '0:10,43:65,88:97'),
    (power.HOMEWORK025_PDF, ':'),
    (power.BACHELOR076_PDF, ':'),
    (power.MASTER072_PDF, ':'),
    (power.BACHELOR090_PDF, ':'),
    (power.BACHELOR037_PDF, '0:10'),
    (power.BACHELOR063_PDF, '10:15'),
    (power.DOCU35_PDF, '0:10'),
    (power.BOOK007_PDF, '0:10'),
    (power.MASTER078_PDF, '0:10'),
    (power.MASTER083_PDF, '0:10'),
    (power.MASTER099_PDF, '0:10'),
    (power.DOCU07_PDF, '0:10'),
    (power.TECHNICAL_024, '0:10'),
]

GENERATE_NO_TOC = [
    (power.DOCU35_PDF, ':'),
    (power.BOOK007_PDF, ':'),
]

GENERATE_NO_TITLE = [
    (power.DOCU35_PDF, ':'),
    (power.BOOK007_PDF, ':'),
]

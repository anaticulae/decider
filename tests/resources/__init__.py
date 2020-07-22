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

BACHELOR37 = power.link(power.BACHELOR037_PDF)
BACHELOR76 = power.link(power.BACHELOR076_PDF)
BACHELOR90 = power.link(power.BACHELOR090_PDF)
DOCU_TWINE = power.link(power.DOCU35_PDF)
LEFTRIGHT = power.link(power.BOOK007_PDF)
MASTER116 = power.link(power.MASTER116_PDF)
MASTER72 = power.link(power.MASTER072_PDF)
MASTER78 = power.link(power.MASTER078_PDF)
MASTER83 = power.link(power.MASTER083_PDF)
MASTER98 = power.link(power.MASTER098_PDF)
MASTER99 = power.link(power.MASTER099_PDF)
PYPORTING = power.link(power.DOCU07_PDF)
TECHNICAL24 = power.link(power.TECHNICAL_024)

TWINE_NO_TITLE_PAGE = power.link(power.DOCU35_PDF, folder='notitle')
TWINE_NO_TOC = power.link(power.DOCU35_PDF, folder='notoc')

TODO = [
    (power.MASTER116_PDF, '0:10,90:115'),
    (power.MASTER098_PDF, '0:10,88:97'),
    (power.BACHELOR076_PDF, ':'),
    (power.MASTER072_PDF, ':'),
    (power.BACHELOR090_PDF, ':'),
    (power.BACHELOR037_PDF, '0:10'),
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

REQURIED_RESOURCES = [
    BACHELOR37,
    BACHELOR76,
    BACHELOR90,
    DOCU_TWINE,
    LEFTRIGHT,
    MASTER116,
    MASTER72,
    MASTER78,
    MASTER83,
    MASTER98,
    MASTER99,
    TECHNICAL24,
    TWINE_NO_TITLE_PAGE,
    TWINE_NO_TOC,
]

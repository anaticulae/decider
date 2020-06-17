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

NO_TITLE_PAGE = os.path.join(GENERATED, 'no_titlepage')
NO_TOC = os.path.join(GENERATED, 'no_toc')

TEST_CONFIG_DATA = os.path.join(decider.ROOT, 'tests/config')

DECIDER_FONTS = os.path.join(TEST_CONFIG_DATA, 'decider_fonts')
assert os.path.exists(DECIDER_FONTS), DECIDER_FONTS

BACHELOR37 = os.path.join(GENERATED, 'bachelor_page_37_tables')
BACHELOR76 = os.path.join(GENERATED, 'bachelor_page76')
BACHELOR90 = os.path.join(GENERATED, 'bachelor_bachelor90')
DOCU_TWINE = os.path.join(GENERATED, 'docu_twine')
LEFTRIGHT = os.path.join(GENERATED, 'book_leftright')
MASTER116 = os.path.join(GENERATED, 'master_page_116_images_toc_formular')
MASTER72 = os.path.join(GENERATED, 'master_page_72_noimages_toc')
MASTER78 = os.path.join(GENERATED, 'master_page_78_images_toc')
MASTER83 = os.path.join(GENERATED, 'master_page_83_noimages_toc')
MASTER98 = os.path.join(GENERATED, 'master_page98')
MASTER99 = os.path.join(GENERATED, 'master_page99')
PYPORTING = os.path.join(GENERATED, 'docu_howto_pyporting')
TECHNICAL = os.path.join(RESOURCES, 'technical')
TECHNICAL24 = os.path.join(GENERATED, 'technical_page_24_color_figures_images')
TWINE_NO_TITLE_PAGE = os.path.join(NO_TITLE_PAGE, 'docu_twine')
TWINE_NO_TOC = os.path.join(NO_TOC, 'docu_twine')

TODO = [
    (power.MASTER116_PDF, '0:10,90:115'),
    (power.BACHELOR076_PDF, ':'),
    (power.MASTER072_PDF, ':'),
    (power.BACHELOR090_PDF, ':'),
    (power.BACHELOR037_PDF, '0:10'),
    (power.DOCU35_PDF, '0:10'),
    (power.BOOK007_PDF, '0:10'),
    (power.MASTER078_PDF, '0:10'),
    (power.MASTER083_PDF, '0:10'),
    (power.MASTER098_PDF, '0:10'),
    (power.MASTER099_PDF, '0:10'),
    (power.DOCU07_PDF, '0:10'),
    (power.TECHNICAL_024, '0:10'),
]

GENERATE_NO_TOC = [
    power.DOCU35_PDF,
    power.BOOK007_PDF
]

GENERATE_NO_TITLE = [
    power.DOCU35_PDF,
    power.BOOK007_PDF
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
    NO_TITLE_PAGE,
    TECHNICAL24,
    TWINE_NO_TITLE_PAGE,
    TWINE_NO_TOC,
]

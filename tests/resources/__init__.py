# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import decider

RESOURCES = os.path.join(decider.ROOT, 'tests/resources')
assert os.path.exists(RESOURCES), RESOURCES

GENERATED = os.path.join(RESOURCES, 'generated')

NO_TITLE_PAGE = os.path.join(GENERATED, 'no_titlepage')
NO_TOC = os.path.join(GENERATED, 'no_toc')

TEST_CONFIG_DATA = os.path.join(decider.ROOT, 'tests/config')

MASTER = os.path.join(RESOURCES, 'master')
BOOK = os.path.join(RESOURCES, 'book')

DECIDER_FONTS = os.path.join(TEST_CONFIG_DATA, 'decider_fonts')
assert os.path.exists(DECIDER_FONTS), DECIDER_FONTS

DOCU = os.path.join(RESOURCES, 'docu')
DOCU_TWINE = os.path.join(DOCU, 'twine.pdf')
DOCU_TWINE_GENERATED = os.path.join(GENERATED, 'docu_twine')

TECHNICAL = os.path.join(RESOURCES, 'technical')
TECHNICAL24 = os.path.join(TECHNICAL, 'page_24_color_figures_images.pdf')
TECHNICAL24_GENERATED = os.path.join(
    GENERATED,
    'technical_page_24_color_figures_images',
)

MASTER_HUGE = os.path.join(MASTER, 'page_116_images_toc_formular.pdf')

MASTER72 = os.path.join(MASTER, 'page_72_noimages_toc.pdf')
MASTER72_GENERATED = os.path.join(
    GENERATED,
    'master_page_72_noimages_toc',
)

MASTER78 = os.path.join(MASTER, 'page_78_images_toc.pdf')
MASTER78_GENERATED = os.path.join(
    GENERATED,
    'master_page_78_images_toc',
)

LEFTRIGHT = os.path.join(BOOK, 'leftright.pdf')
LEFTRIGHT_GENERATED = os.path.join(
    GENERATED,
    'book_leftright',
)

TWINE_NO_TITLE_PAGE = os.path.join(NO_TITLE_PAGE, 'docu_twine')
TWINE_NO_TOC = os.path.join(NO_TOC, 'docu_twine')

TODO = [
    DOCU_TWINE,
    LEFTRIGHT,
    MASTER72,
    MASTER78,
    TECHNICAL24,
]

REQURIED_RESOURCES = [
    BOOK,
    DOCU_TWINE,
    DOCU_TWINE_GENERATED,
    LEFTRIGHT,
    LEFTRIGHT_GENERATED,
    MASTER72,
    MASTER72_GENERATED,
    MASTER78,
    MASTER78_GENERATED,
    MASTER_HUGE,
    NO_TITLE_PAGE,
    TECHNICAL24,
    TECHNICAL24_GENERATED,
    TWINE_NO_TITLE_PAGE,
    TWINE_NO_TOC,
]

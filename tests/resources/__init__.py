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

GENERATED = os.path.join(RESOURCES, 'generated')

NO_TITLE_PAGE = os.path.join(GENERATED, 'no_titlepage')

TEST_CONFIG_DATA = os.path.join(decider.ROOT, 'tests/config')

MASTER = os.path.join(RESOURCES, 'master')

DECIDER_FONTS = os.path.join(TEST_CONFIG_DATA, 'decider_fonts')
assert os.path.exists(DECIDER_FONTS), DECIDER_FONTS

DOCU = os.path.join(RESOURCES, 'docu')
DOCU_TWINE = os.path.join(DOCU, 'twine.pdf')
DOCU_TWINE_GENERATED = os.path.join(GENERATED, 'docu_twine')

TECHNICAL = os.path.join(RESOURCES, 'technical')
TECHNICAL_24PAGES = os.path.join(TECHNICAL, 'page_24_color_figures_images.pdf')
TECHNICAL_24PAGES_GENERATED = os.path.join(
    GENERATED,
    'technical_page_24_color_figures_images',
)

MASTER_HUGE = os.path.join(MASTER, 'page_116_images_toc_formular.pdf')

MASTER_72_PAGES_NOIMAGES = os.path.join(MASTER, 'page_72_noimages_toc.pdf')
MASTER_72_PAGES_NOIMAGES_GENERATED = os.path.join(
    GENERATED,
    'master_page_72_noimages_toc',
)

MASTER_78_PAGES_IMAGES = os.path.join(MASTER, 'page_78_images_toc.pdf')
MASTER_78_PAGES_IMAGES_GENERATED = os.path.join(
    GENERATED,
    'master_page_78_images_toc',
)

TODO = [
    DOCU_TWINE,
    MASTER_72_PAGES_NOIMAGES,
    MASTER_78_PAGES_IMAGES,
    TECHNICAL_24PAGES,
]

REQURIED_RESOURCES = [
    DOCU_TWINE,
    DOCU_TWINE_GENERATED,
    MASTER_72_PAGES_NOIMAGES,
    MASTER_72_PAGES_NOIMAGES_GENERATED,
    MASTER_78_PAGES_IMAGES,
    MASTER_78_PAGES_IMAGES_GENERATED,
    MASTER_HUGE,
    NO_TITLE_PAGE,
    TECHNICAL_24PAGES,
    TECHNICAL_24PAGES_GENERATED,
]

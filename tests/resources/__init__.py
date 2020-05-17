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

BACHELOR = os.path.join(RESOURCES, 'bachelor')
MASTER = os.path.join(RESOURCES, 'master')
BOOK = os.path.join(RESOURCES, 'book')

DECIDER_FONTS = os.path.join(TEST_CONFIG_DATA, 'decider_fonts')
assert os.path.exists(DECIDER_FONTS), DECIDER_FONTS

DOCU = os.path.join(RESOURCES, 'docu')
DOCU_TWINE_PDF = os.path.join(DOCU, 'twine.pdf')
DOCU_TWINE = os.path.join(GENERATED, 'docu_twine')

TECHNICAL = os.path.join(RESOURCES, 'technical')
TECHNICAL24_PDF = os.path.join(TECHNICAL, 'page_24_color_figures_images.pdf')
TECHNICAL24 = os.path.join(GENERATED, 'technical_page_24_color_figures_images')

MASTER116_PDF = os.path.join(MASTER, 'page_116_images_toc_formular.pdf')
MASTER116 = os.path.join(GENERATED, 'master_page_116_images_toc_formular')

BACHELOR37_PDF = os.path.join(BACHELOR, 'page_37_tables.pdf')
BACHELOR37 = os.path.join(GENERATED, 'bachelor_page_37_tables')

BACHELOR76_PDF = os.path.join(BACHELOR, 'page76.pdf')
BACHELOR76 = os.path.join(GENERATED, 'bachelor_page76')

MASTER72_PDF = os.path.join(MASTER, 'page_72_noimages_toc.pdf')
MASTER72 = os.path.join(GENERATED, 'master_page_72_noimages_toc')

MASTER78_PDF = os.path.join(MASTER, 'page_78_images_toc.pdf')
MASTER78 = os.path.join(GENERATED, 'master_page_78_images_toc')

MASTER83_PDF = os.path.join(MASTER, 'page_83_noimages_toc.pdf')
MASTER83 = os.path.join(GENERATED, 'master_page_83_noimages_toc')

MASTER98_PDF = os.path.join(MASTER, 'page98.pdf')
MASTER98 = os.path.join(GENERATED, 'master_page98')

MASTER99_PDF = os.path.join(MASTER, 'page99.pdf')
MASTER99 = os.path.join(GENERATED, 'master_page99')

PYPORTING_PDF = os.path.join(DOCU, 'howto_pyporting.pdf')
PYPORTING = os.path.join(GENERATED, 'docu_howto_pyporting')

LEFTRIGHT_PDF = os.path.join(BOOK, 'leftright.pdf')
LEFTRIGHT = os.path.join(GENERATED, 'book_leftright')

TWINE_NO_TITLE_PAGE = os.path.join(NO_TITLE_PAGE, 'docu_twine')
TWINE_NO_TOC = os.path.join(NO_TOC, 'docu_twine')

TODO = [
    (BACHELOR76_PDF, ':'),
    (MASTER72_PDF, ':'),
    (BACHELOR37_PDF, '0:10'),
    (DOCU_TWINE_PDF, '0:10'),
    (LEFTRIGHT_PDF, '0:10'),
    (MASTER78_PDF, '0:10'),
    (MASTER83_PDF, '0:10'),
    (MASTER98_PDF, '0:10'),
    (MASTER99_PDF, '0:10'),
    (MASTER116_PDF, '0:10'),
    (PYPORTING_PDF, '0:10'),
    (TECHNICAL24_PDF, '0:10'),
]

GENERATE_NO_TOC = [
    DOCU_TWINE_PDF,
    LEFTRIGHT_PDF,
]

GENERATE_NO_TITLE = [
    DOCU_TWINE_PDF,
    LEFTRIGHT_PDF,
]

REQURIED_RESOURCES = [
    BACHELOR,
    BACHELOR37,
    BACHELOR37_PDF,
    BACHELOR76,
    BACHELOR76_PDF,
    BOOK,
    DOCU_TWINE,
    DOCU_TWINE_PDF,
    LEFTRIGHT,
    LEFTRIGHT_PDF,
    MASTER116,
    MASTER116_PDF,
    MASTER72,
    MASTER72_PDF,
    MASTER78,
    MASTER78_PDF,
    MASTER83,
    MASTER83_PDF,
    MASTER98,
    MASTER98_PDF,
    MASTER99,
    MASTER99_PDF,
    NO_TITLE_PAGE,
    TECHNICAL24,
    TECHNICAL24_PDF,
    TWINE_NO_TITLE_PAGE,
    TWINE_NO_TOC,
]

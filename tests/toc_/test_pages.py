# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import decider_toc.pages as dtp
import tests


def test_toc_pages_validate():
    toc = tests.tableofcontent(power.link(power.TECH024_PDF))
    validated = dtp.validate(toc)  # pylint:disable=W0612

    assert validated == [], validated


def test_toc_pages_validate_with_errors():
    toc = tests.tableofcontent(power.link(power.TECH024_PDF))

    # introduce some errors
    toc.children[1].page = 10
    toc.children[5].page = 20
    validated = dtp.validate(toc)  # pylint:disable=W0612
    assert len(validated) == 2, validated

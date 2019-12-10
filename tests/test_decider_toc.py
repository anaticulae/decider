# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.path
import iamraw
import pytest
import serializeraw

import decider.features.toc as dft
import decider.toc.level as dtl
import tests.resources


def tableofcontent(path: str) -> iamraw.Toc:
    path = groupme.path.toc(path)
    result = serializeraw.load_toc(path)
    return result


def lint(path: str):
    toc = tableofcontent(path)
    linter = dft.create_linter()
    dft.linting(toc=toc, linter=linter)
    user, _ = linter.result(unique=False)
    failures = sorted(messageids(user))
    return failures


def test_toc_extraction_no_toc():  # pylint:disable=W0621
    expected_failures = [dft.MISSING_TOC_ID]

    failures = lint(tests.resources.TWINE_NO_TOC)

    assert failures == expected_failures, str(failures)


def test_toc_extraction():  # pylint:disable=W0621
    expected_failures = []

    failures = lint(tests.resources.TECHNICAL_24PAGES_GENERATED)

    assert failures == expected_failures, str(failures)


def messageids(items):
    result = [item.msgid for item in items]
    return result


@pytest.mark.parametrize('source, invalids', [
    pytest.param(
        tests.resources.TECHNICAL_24PAGES_GENERATED,
        1,
        id='technical24',
    ),
    pytest.param(
        tests.resources.MASTER_78_PAGES_IMAGES_GENERATED,
        3,
        marks=pytest.mark.xfail(reason='fix toc parser'),
        id='master78',
    ),
    pytest.param(
        tests.resources.MASTER_72_PAGES_NOIMAGES_GENERATED,
        0,
        id='master72',
    ),
])
def test_toc_validate_children(source, invalids):
    toc = tableofcontent(source)
    validated = dtl.validate_children(toc)
    assert len(validated) == invalids, str(len(validated))


@pytest.mark.parametrize('source, todeep', [
    pytest.param(
        tests.resources.TECHNICAL_24PAGES_GENERATED,
        14,
        id='technical24',
    ),
    pytest.param(
        tests.resources.MASTER_72_PAGES_NOIMAGES_GENERATED,
        6,
        id='master72',
    ),
])
def test_toc_validate_deepness(source, too_deep):
    toc = tableofcontent(source)
    maxdeep = 2
    validated = dtl.validate_deepness(toc, maxdeep=maxdeep)
    # `too_deep` items with 1.2.3
    assert len(validated) == too_deep

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import pytest

import decider_toc.features.basic as dtfb
import decider_toc.features.complexity as dtfc
import decider_toc.features.rules as dtfr
import decider_toc.level as dtl
import tests
import tests.resources

TECHNICAL24_INVALID_CHILDREN = 1
TECHNICAL24_INVALID_CHILDREN_TO_LONG = 1
TECHNICAL24_TOO_DEEP = 14


def test_toc_extraction_no_toc():
    expected_failures = [1300]
    failures = lint(tests.resources.TWINE_NO_TOC, dtfb)
    assert failures == expected_failures, str(failures)


def test_toc_invalid_children(monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(dtl, 'MAX_TOC_DEEPNESS', 2)
        failures = lint(tests.resources.TECHNICAL24, dtfr)
    failures = len(failures)
    assert failures == TECHNICAL24_INVALID_CHILDREN, str(failures)


def test_toc_to_deep(monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(dtl, 'MAX_TOC_DEEPNESS', 2)
        failures = lint(tests.resources.TECHNICAL24, dtfc)
    failures = len([item for item in failures if item in (1351, 1382)])
    expected = sum([
        TECHNICAL24_INVALID_CHILDREN_TO_LONG,
        TECHNICAL24_TOO_DEEP,
    ])
    assert failures == expected, str(failures)


@pytest.mark.parametrize(
    'source, invalids',
    [
        pytest.param(
            tests.resources.TECHNICAL24,
            TECHNICAL24_INVALID_CHILDREN,
            id='technical24',
        ),
        # TODO: MASTER78_PDF PARSER IS BUGGY RIGHT NOW
        pytest.param(
            tests.resources.MASTER78,
            3,
            id='master78',
            marks=pytest.mark.xfail(
                reason='investigate here, expected seems not to be correct'),
        ),
        pytest.param(
            tests.resources.MASTER72,
            0,
            id='master72',
        ),
    ])
def test_toc_validate_children(source, invalids):
    toc = tests.tableofcontent(source)
    validated = dtl.validate_children(toc)
    assert len(validated) == invalids, str(len(validated))


@pytest.mark.parametrize('source, too_deep', [
    pytest.param(
        tests.resources.TECHNICAL24,
        TECHNICAL24_TOO_DEEP,
        id='technical24',
    ),
    pytest.param(
        tests.resources.MASTER72,
        6,
        id='master72',
        marks=pytest.mark.xfail(
            reason='fix toc extractor, shrink to first pages'),
    ),
])
def test_toc_validate_deepness(source, too_deep):
    toc = tests.tableofcontent(source)
    maxdeep = 2
    validated = dtl.validate_deepness(toc, maxdeep=maxdeep)
    # `too_deep` items with 1.2.3
    assert len(validated) == too_deep


def lint(path: str, module):
    toc = tests.tableofcontent(path)
    linter = protocol.from_module(module.__name__)
    module.linting(toc=toc, linter=linter)
    result = linter.result(unique=False)
    failures = sorted(item.msgid for item in result)
    return failures

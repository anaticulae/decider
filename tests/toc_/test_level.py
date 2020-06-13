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

import decider_toc.features.complexity as dtfc
import decider_toc.features.rules as dtfr
import decider_toc.level as dtl
import tests
import tests.resources

TECHNICAL24_INVALID_CHILDREN = 1
TECHNICAL24_INVALID_CHILDREN_TO_LONG = 1
TECHNICAL24_TOO_DEEP = 14


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


def master78_too_few_children(invalid):
    # TODO: MASTER78_PDF PARSER IS BUGGY RIGHT NOW
    assert invalid[0].title == 'Grundsätzliche Anforderungen'
    assert invalid[1].title == 'Anbindung der Bussysteme'
    assert invalid[2].title == 'Auswahl passender Busgeräte'


@pytest.mark.parametrize('source, invalids, validate', [
    pytest.param(
        tests.resources.TECHNICAL24,
        TECHNICAL24_INVALID_CHILDREN,
        None,
        id='technical24',
    ),
    pytest.param(
        tests.resources.MASTER78,
        3,
        master78_too_few_children,
        id='master78',
        marks=pytest.mark.xfail(reason='toc extraction does not work properly'),
    ),
    pytest.param(
        tests.resources.MASTER72,
        0,
        None,
        id='master72',
    ),
])
def test_toc_too_few_children(source, invalids, validate):
    toc = tests.tableofcontent(source)
    validated = dtl.validate_children(toc)
    assert len(validated) == invalids, str(len(validated))
    if not validate:
        return
    validate(validated)


# yapf:disable
@pytest.mark.parametrize('source, too_deep', [
    pytest.param(tests.resources.TECHNICAL24, TECHNICAL24_TOO_DEEP, id='technical24'),
    pytest.param(tests.resources.MASTER72, 6, id='master72'),
])
# yapf:enable
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

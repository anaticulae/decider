# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.path
import serializeraw

import decider.features.toc as dft
import tests.resources


def lint(path: str):
    toc = groupme.path.toc(path)
    toc = serializeraw.load_toc(toc)
    linter = dft.create_linter()
    dft.linting(toc=toc, linter=linter)
    user, _ = linter.result(unique=True)
    failures = messageids(user)
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

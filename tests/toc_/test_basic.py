# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol

import decider_toc.features.basic as dtfb
import tests


def test_toc_extraction_no_toc():
    expected_failures = [1300, 1301]
    failures = lint(power.link(power.DOCU35_PDF, folder='notoc'), dtfb)
    assert failures == expected_failures, str(failures)


def lint(path: str, module):
    toc = tests.tableofcontent(path)
    linter = protocol.from_module(module.__name__)
    driver = protocol.driver(
        toc=toc,
        outlines=None,
    )
    linter.run(driver=driver)
    result = linter.result(unique=False)
    failures = sorted(item.msgid for item in result)
    return failures

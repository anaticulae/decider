# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import protoerror
import pytest
import utilotest

import tests.footnote_


def home18(findings):
    assert protoerror.count_findings(findings, 2017) == 8
    # assert protoerror.count_findings(findings, 2018) == 1
    assert not protoerror.count_findings(findings, 2018)  # TODO CHANGE LATER


def bachelor128(findings):
    # TODO: MERGE THIS FINDING?
    assert protoerror.count_findings(findings, 2016) == 26


def bachelor076(findings):
    assert findings
    # regression
    ebd_duplicated = protoerror.count_findings(findings, 2019)
    assert not ebd_duplicated


# def bachelor85(findings):
#     # TODO: ENABLE AFTER FIXING RAWMAKER
#     assert protoerror.count_findings(findings, 2019)


@pytest.mark.parametrize('source, expected', [
    pytest.param(hoverpower.HOME018_PDF, home18, id='home18'),
    pytest.param(hoverpower.BACHELOR076_PDF, bachelor076, id='bachelor076'),
    pytest.param(hoverpower.BACHELOR128_PDF, bachelor128, id='bachelor128'),
])
def test_footnote_rules_improvement(source, expected, td, mp):
    """Run decider"""
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    cmd = f'-i {source} --rules'
    tests.footnote_.run(cmd, mp=mp)
    loaded = protoerror.findings_from_path(td.tmpdir)
    findings = protoerror.flat(loaded)
    expected(findings)

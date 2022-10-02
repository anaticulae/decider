# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import pytest

import tests.footnote_


def home18(findings):
    assert protocol.count_findings(findings, 2017) == 8
    # assert protocol.count_findings(findings, 2018) == 1
    assert not protocol.count_findings(findings, 2018)  # TODO CHANGE LATER


def bachelor128(findings):
    # TODO: MERGE THIS FINDING?
    assert protocol.count_findings(findings, 2016) == 26


def bachelor076(findings):
    assert findings
    # regression
    ebd_duplicated = protocol.count_findings(findings, 2019)
    assert not ebd_duplicated


# def bachelor85(findings):
#     # TODO: ENABLE AFTER FIXING RAWMAKER
#     assert protocol.count_findings(findings, 2019)


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.HOME018_PDF, home18, id='home18'),
    pytest.param(power.BACHELOR076_PDF, bachelor076, id='bachelor076'),
    pytest.param(power.BACHELOR128_PDF, bachelor128, id='bachelor128'),
])
def test_footnote_rules_improvement(source, expected, td, mp):
    """Run decider"""
    source = power.link(source)
    cmd = f'-i {source} --rules'
    tests.footnote_.run(cmd, mp=mp)
    loaded = protocol.findings_from_path(td.tmpdir)
    findings = protocol.flat(loaded)
    expected(findings)

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import pytest

import tests.footnote_


def home18(findings):
    findings = protocol.flat(findings)
    assert protocol.count_findings(findings, 2017) == 8
    assert protocol.count_findings(findings, 2018) == 1


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.HOME018_PDF, home18, id='home18'),
])
def test_footnote_rules_improvement(source, expected, testdir, monkeypatch):
    """Run decider"""
    source = power.link(source)
    cmd = f'-i {source} --rules'
    tests.footnote_.run(cmd, monkeypatch=monkeypatch)
    loaded = protocol.findings_from_path(testdir.tmpdir)
    expected(loaded)

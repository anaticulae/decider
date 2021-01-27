# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import decider_footnote.path
import tests.footnote_


def test_footnote_uppercase_start_master89_page40(testdir, monkeypatch):
    """Support quotation start char, see: 2001"""
    cmd = f'-i {power.link(power.MASTER089_PDF)} -o {testdir.tmpdir} --rules'
    tests.footnote_.run(cmd, monkeypatch=monkeypatch)

    rules = decider_footnote.path.rules(testdir.tmpdir)
    result = serializeraw.load_findings(rules, 2001)

    result = [finding for finding in result if finding.location.page == 40]
    assert not result


def test_footnote_dot_end_master89_page46(testdir, monkeypatch):
    """Support quotation end char, see: 2002"""
    cmd = f'-i {power.link(power.MASTER089_PDF)} -o {testdir.tmpdir} --rules'
    tests.footnote_.run(cmd, monkeypatch=monkeypatch)

    rules = decider_footnote.path.rules(testdir.tmpdir)
    result = serializeraw.load_findings(rules, 2002)

    result = [finding for finding in result if finding.location.page == 46]
    assert not result

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import decider_footnote.path
import tests.footnote_


def test_footnote_uppercase_start_master89_page40(testdir, monkeypatch):  ## pylint:disable=W0621
    """Support quotation start char, see: 2001"""
    root = str(testdir)

    cmd = f'-i {power.link(power.MASTER089_PDF)} -o {root} --rules'
    tests.footnote_.run(cmd, monkeypatch=monkeypatch)

    rules = decider_footnote.path.rules(root)

    result = serializeraw.load_findings(rules, 2001)

    result = [finding for finding in result if finding.location.page == 40]
    assert not result

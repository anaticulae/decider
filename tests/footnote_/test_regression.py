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
import serializeraw

import decider_footnote.path
import tests.footnote_


def test_footnote_separator_distance(testdir, monkeypatch):
    cmd = f'-i {power.link(power.MASTER155_PDF)} -o {testdir.tmpdir} --rules'
    tests.footnote_.run(cmd, monkeypatch=monkeypatch)

    rules = decider_footnote.path.rules(testdir.tmpdir)
    rules = serializeraw.load_findings(rules)

    # TODO: DECREASE SEPARATOR_FOOTNOTE_MAX_DISTANCE to verify that
    # enable after upgrading protocol
    # -hv:separator_footnote_max_distance=0
    # linting works
    result = protocol.count_findings(rules, 2016)
    assert not result

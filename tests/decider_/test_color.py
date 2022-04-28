# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import utilatest

import tests.decider_


@utilatest.requires(power.BACHELOR051_PDF)
def test_color_bachelor051(testdir, monkeypatch):
    source = power.link(power.BACHELOR051_PDF)
    cmd = f'-i {source} --color --pages=20'
    tests.decider_.run(cmd, monkeypatch=monkeypatch)
    findings = protocol.findings_from_path(testdir.tmpdir, msgid=10600)
    assert findings[0].page == 20
    findings = findings[0].content
    assert len(findings) == 4

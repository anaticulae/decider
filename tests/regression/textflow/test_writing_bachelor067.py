# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import utilatest

import tests.textflow_


@utilatest.requires(power.BACHELOR067_PDF)
def test_reg_writing_bachelor067(testdir, monkeypatch):
    """A very long sentence is detected, which is a result of bad parsed
    list.
    """
    source = power.link(power.BACHELOR067_PDF)
    cmd = f'-i {source} --writing --pages=54'
    tests.textflow_.run(cmd, monkeypatch=monkeypatch)
    findings = protocol.findings_from_path(testdir.tmpdir, msgid=7600)
    content = findings[0].content
    # two `man` findings
    assert len(content) == 2

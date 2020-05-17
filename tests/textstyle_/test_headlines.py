# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol

import decider_textstyle.path
import tests.resources
import tests.textstyle_


def test_decider_headlines(testdir, monkeypatch):
    master72 = tests.resources.MASTER72
    tests.textstyle_.run(
        f'--headlines -i {master72} --pages=2:20',
        monkeypatch=monkeypatch,
    )
    path = decider_textstyle.path.headlines(testdir.tmpdir)
    findings = protocol.load_result(path)
    # no font size error
    assert not findings


def test_decider_headlines_master72_all(testdir, monkeypatch):
    master72 = tests.resources.MASTER72
    tests.textstyle_.run(
        f'--headlines -i {master72} --pages=3:65',
        monkeypatch=monkeypatch,
    )
    path = decider_textstyle.path.headlines(testdir.tmpdir)
    findings = protocol.load_result(path)
    # no font size error
    assert not findings

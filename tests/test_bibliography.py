# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol

import decider.path
import tests
import tests.resources


def test_bib_sorting_master98(testdir, monkeypatch):
    source = tests.resources.MASTER98
    cmd = f'-i {source} --bibliography'
    tests.run_decider(cmd, monkeypatch=monkeypatch)

    path = decider.path.bibliography_user(testdir.tmpdir)
    result = protocol.select_findings(protocol.load_result(path), msgid=6000)
    assert len(result) == 1

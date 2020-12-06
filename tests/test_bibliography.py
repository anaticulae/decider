# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import pytest
import serializeraw

import decider.path
import tests


def test_bib_sorting_master98(testdir, monkeypatch):
    source = power.link(power.MASTER098_PDF)
    cmd = f'-i {source} --bibliography'
    tests.run_decider(cmd, monkeypatch=monkeypatch)

    path = decider.path.bibliography_user(testdir.tmpdir)
    result = protocol.select_findings(
        serializeraw.load_findings(path),
        msgid=6000,
    )
    assert len(result) == 1


@pytest.mark.xfail(reason='improve bib parser')
def test_bib_sorting_master116(testdir, monkeypatch):
    source = power.link(power.MASTER116_PDF)
    cmd = f'-i {source} --bibliography'
    tests.run_decider(cmd, monkeypatch=monkeypatch)

    path = decider.path.bibliography_user(testdir.tmpdir)
    result = protocol.select_findings(
        serializeraw.load_findings(path),
        msgid=6000,
    )
    assert not result  # TODO: VALIDATE LATER

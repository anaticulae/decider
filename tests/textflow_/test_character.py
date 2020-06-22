# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol

import decider_textflow.path
import tests.resources
import tests.textflow_


def decider_textflow_character(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids=None,
):
    tests.textflow_.run(
        f'--writing -i {source} --pages={pages} --character',
        monkeypatch=monkeypatch,
    )
    path = decider_textflow.path.character_linted(testdir.tmpdir)
    findings = protocol.load_result(path, msgids=msgids)
    return findings


def test_textflow_character_space_before_comma(testdir, monkeypatch):
    source = tests.resources.BACHELOR90
    pages = '30'
    findings = decider_textflow_character(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids=7650,
    )
    assert len(findings) == 1

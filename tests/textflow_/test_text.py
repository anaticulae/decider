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


def decide_textflow(source, pages, testdir, monkeypatch):
    tests.textflow_.run(
        f'--writing -i {source} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    path = decider_textflow.path.writing_linted(testdir.tmpdir)
    findings = protocol.load_result(path)
    return findings


def test_decider_textflow_bachelor67_perspective(testdir, monkeypatch):
    source = tests.resources.BACHELOR76
    pages = ':'
    findings = decide_textflow(source, pages, testdir, monkeypatch)
    # TODO: decrement to 4 after including quotation check
    assert len(findings) == 5

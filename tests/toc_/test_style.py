# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol

import tests.resources


def test_toc_style_bachelor76_duplicated_words(testdir, monkeypatch):
    source = tests.resources.BACHELOR76
    tests.toc_.run(f'-i {source} --style', monkeypatch=monkeypatch)

    findings = protocol.findings_from_path(testdir.tmpdir)
    findings = findings[0].content

    duplicated_words = select_finding(findings, msgid=1380)
    assert len(duplicated_words) == 1, str(duplicated_words)
    assert 'Industrie 4.0' in duplicated_words[0].solution.description


def select_finding(findings, msgid: int):
    # TODO: REPLACE WITH PROTCOL CODE
    return [item for item in findings if item.msgid == msgid]

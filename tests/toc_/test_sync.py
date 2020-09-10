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

import tests


def test_toc_bachelor90_toc_document_sync(testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    tests.toc_.run(f'-i {source} --sync', monkeypatch=monkeypatch)

    findings = protocol.findings_from_path(testdir.tmpdir)
    assert len(tests.select(findings, 1330)) == 1

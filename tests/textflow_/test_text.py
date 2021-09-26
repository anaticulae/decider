# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import decider_textflow.features.writing
import decider_textflow.path
import tests.textflow_


def decide_textflow(source, pages, testdir, monkeypatch, msgids=None):
    tests.textflow_.run(
        f'--writing -i {source} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    path = decider_textflow.path.writing_linted(testdir.tmpdir)
    findings = serializeraw.load_findings(path, msgids=msgids)
    return findings


@utilatest.longrun
def test_dtf_bachelor67_perspective(testdir, monkeypatch):
    source = power.link(power.BACHELOR076_PDF)
    pages = ':'
    findings = decide_textflow(source, pages, testdir, monkeypatch)
    assert len(findings) == 4  # VALIDATED


def test_dtf_master72_writing_quotation(testdir, monkeypatch):
    """Do not detect errors in perspective inside quotations."""
    source = power.link(power.MASTER072_PDF)
    pages = '12:15'
    findings = decide_textflow(source, pages, testdir, monkeypatch, msgids=7600)
    assert not findings


EXPECTED = """Norbert Schneider &#40;2012&#41; sieht die „Selbstentblößung“ in \
den Medien als Folge einer Individualisierung und als Ersatz für die verlorene \
Bestätigung aus einem Kollektiv, dem man angehörte, z.B."""


def test_dtf_master72_merge_token_correctly(testdir, monkeypatch):
    """Do not detect errors in perspective inside quotations."""
    source = power.link(power.MASTER072_PDF)
    pages = '16'
    findings = decide_textflow(source, pages, testdir, monkeypatch, msgids=7600)
    assert len(findings) == 1
    description = findings[0].solution.description
    assert EXPECTED in description


@utilatest.requires(power.MASTER072_PDF)
def test_dtf_master72_text_too_long(testdir, monkeypatch):
    """Detect sentence which are too long."""
    source = power.link(power.MASTER072_PDF)
    pages = '3:6'
    with monkeypatch.context() as context:
        context.setattr(
            decider_textflow.features.writing,
            'MAX_SENTENCE_LENGTH',
            100,
        )
        findings = decide_textflow(
            source,
            pages,
            testdir,
            monkeypatch,
            msgids=7605,
        )
    assert len(findings) == 20

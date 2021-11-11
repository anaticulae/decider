# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utilatest

import decider_textflow.features.writing
import decider_textflow.path
import tests.textflow_


def decide_textflow(source, testdir, monkeypatch, pages=None, msgids=None):
    utilatest.fixture_requires(source)
    source = power.link(source)
    cmd = f'--writing -i {source} '
    if pages:
        cmd += f'--pages={pages}'
    tests.textflow_.run(cmd, monkeypatch=monkeypatch)
    path = decider_textflow.path.writing_linted(testdir.tmpdir)
    findings = serializeraw.load_findings(path, msgids=msgids)
    return findings


@pytest.mark.xfail(reason='wir in quotation detected')
@utilatest.longrun
def test_dtf_bachelor76_perspective(testdir, monkeypatch):
    source = power.BACHELOR076_PDF
    findings = decide_textflow(source, testdir, monkeypatch, msgids=7600)
    assert len(findings) == 5  # VALIDATED


@pytest.mark.xfail(reason='man in quotation')
def test_dtf_master72_writing_quotation(testdir, monkeypatch):
    """Do not detect errors in perspective inside quotations."""
    source = power.MASTER072_PDF
    pages = '12:15'
    findings = decide_textflow(source, testdir, monkeypatch, pages, msgids=7600)
    assert not findings


EXPECTED = """Norbert Schneider &#40;2012&#41; sieht die „Selbstentblößung“ in \
den Medien als Folge einer Individualisierung und als Ersatz für die verlorene \
Bestätigung aus einem Kollektiv, dem man angehörte, z.B."""


def test_dtf_master72_merge_token_correctly(testdir, monkeypatch):
    """Do not detect errors in perspective inside quotations."""
    source = power.MASTER072_PDF
    pages = '16'
    findings = decide_textflow(source, testdir, monkeypatch, pages, msgids=7600)
    assert len(findings) == 1
    description = findings[0].solution.description
    assert EXPECTED in description


def test_dtf_master72_text_too_long(testdir, monkeypatch):
    """Detect sentence which are too long."""
    source = power.MASTER072_PDF
    pages = '3:6'
    with monkeypatch.context() as context:
        context.setattr(
            decider_textflow.features.writing,
            'SENTENCE_LENGTH_MAX',
            100,
        )
        findings = decide_textflow(
            source,
            testdir,
            monkeypatch,
            pages=pages,
            msgids=7605,
        )
    assert len(findings) == 20


def test_writing_text_statistics(testdir, monkeypatch):
    source = power.MASTER110_PDF
    findings = decide_textflow(
        source,
        testdir,
        monkeypatch,
        msgids=7616,
    )
    assert len(findings) == 1


def test_writing_repeating_sentence_start(testdir, monkeypatch):
    source = power.MASTER110_PDF
    findings = decide_textflow(
        source,
        testdir,
        monkeypatch,
        msgids=7611,
    )
    assert len(findings) == 23  # NOT VALIDATED


def test_writing_repeating_sentence_pattern(testdir, monkeypatch):
    source = power.MASTER110_PDF
    with monkeypatch.context() as context:
        context.setattr(
            decider_textflow.features.writing,
            'SENTENCE_PATTERN_WINDOW',
            3,
        )
        findings = decide_textflow(
            source,
            testdir,
            monkeypatch,
            msgids=7610,
        )
    assert len(findings) == 9  # NOT VALIDATED

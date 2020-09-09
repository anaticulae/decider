# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw

import decider_textflow.path
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
    findings = serializeraw.load_findings(path, msgids=msgids)
    return findings


def test_textflow_character_space_before_comma(testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    pages = '30'
    findings = decider_textflow_character(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids=7650,
    )
    assert len(findings) == 1


def test_textflow_character_missing_space_after_comma(testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    pages = ':'
    findings = decider_textflow_character(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids=7651,
    )
    assert len(findings) == 2


def test_textflow_character_space_before_square_bracket(testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    pages = ':'
    findings = decider_textflow_character(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids=7652,
    )
    assert len(findings) == 2


def test_textflow_character_space_after_square_bracket(testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    pages = ':'
    findings = decider_textflow_character(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids=7653,
    )
    assert len(findings) == 2


def test_textflow_character_missing_space_before_semicolon(
        testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    pages = ':'
    findings = decider_textflow_character(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids=7654,
    )
    assert len(findings) == 12  # TODO: CHANGE TO 13


@pytest.mark.xfail(reason='require line formula inside parser')
def test_character_missing_space_after_comma_master116_page23(
        testdir,
        monkeypatch,
):
    """False positve comma detection. TODO: In the current
    implementation `𝑐𝑤,anfang=0.23` is detected as an false positiv
    error. After introduce a inline formula detector, this problem can
    be solved."""
    source = power.link(power.MASTER116_PDF)
    pages = 23
    findings = decider_textflow_character(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids=7651,
    )
    assert not findings

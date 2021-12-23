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

import decider_textflow.path
import tests.textflow_


def decide_textflow(source, pages, testdir, monkeypatch):
    tests.textflow_.run(
        f'--docref -i {source} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    path = decider_textflow.path.docref_linted(testdir.tmpdir)
    findings = serializeraw.load_findings(path)
    return findings


@pytest.mark.xfail(reason='invalid docref')
def test_dtf_bachelor76_docref_negative(testdir, monkeypatch):
    """This document contains only valid references, therefore we do not
    detect any missing references."""
    source = power.link(power.BACHELOR076_PDF)
    pages = '0:30'
    findings = decide_textflow(source, pages, testdir, monkeypatch)
    assert not findings


@pytest.mark.xfail(reason='broken test')
def test_dtf_master75_docref(testdir, monkeypatch):
    # TODO: DESCRIBE PURPOSE OF TEST
    source = power.link(power.MASTER075_PDF)
    findings = decide_textflow(source, ':', testdir, monkeypatch)
    assert not findings  # may changes later


def test_dtf_bachelor56page15_tableref(testdir, monkeypatch):
    """Verify that `s. Tab. 1` matches with `Tabelle 1`"""
    source = power.link(power.BACHELOR056_PDF)
    pages = '15'
    findings = decide_textflow(source, pages, testdir, monkeypatch)
    assert not findings

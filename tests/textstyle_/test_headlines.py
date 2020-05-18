# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol

import decider_textstyle.path
import tests.resources
import tests.textstyle_


def decide_headline_style(source, pages, testdir, monkeypatch):
    tests.textstyle_.run(
        f'--headlines -i {source} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    path = decider_textstyle.path.headlines(testdir.tmpdir)
    findings = protocol.load_result(path)
    return findings


def test_decider_headlines(testdir, monkeypatch):
    source = tests.resources.MASTER72
    pages = '2:20'
    findings = decide_headline_style(source, pages, testdir, monkeypatch)
    # no font size error
    assert not findings


def test_decider_headlines_master72_all(testdir, monkeypatch):
    source = tests.resources.MASTER72
    pages = '3:65'
    findings = decide_headline_style(source, pages, testdir, monkeypatch)
    # no font size error
    assert not findings


def test_decider_headlines_bachelor76(testdir, monkeypatch):
    # TODO: EXTEND THIS TESTS, specify expected findings
    source = tests.resources.BACHELOR76
    pages = '4:67'
    findings = decide_headline_style(source, pages, testdir, monkeypatch)
    expected = 49  # not correct, but indicates that algo changed

    assert len(findings) == expected

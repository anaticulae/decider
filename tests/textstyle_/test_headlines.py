# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import doctextstyle.data
import doctextstyle.serialize
import protocol
import pytest

import decider_textstyle.path
import tests
import tests.resources
import tests.textstyle_

MASTER_72_DOCSTYLE = doctextstyle.data.DocTextStyle(
    h1_size=15.96,
    h1_after=135.93 - 88.67,
    h2_size=14.04,
    h2_before=190.37 - 125.73,
    h2_after=224.01 - 190.37,
)

BACHELOR_76_DOCSTYLE = doctextstyle.data.DocTextStyle(
    h1_after=132.18 - 92.87,
    h1_size=15.96,
    h2_after=529.1 - 485.39,
    h2_before=485.39 - 426.84,
    h2_size=12.96,
)

# disable font style linting
NO_STYLE = doctextstyle.data.DocTextStyle()


def decide_headline_style(source, pages, style, testdir, monkeypatch):
    tests.textstyle_.write_docstyle(style, testdir.tmpdir)
    tests.textstyle_.run(
        f'--headlines -i {testdir.tmpdir} -i {source} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    path = decider_textstyle.path.headlines(testdir.tmpdir)
    findings = protocol.load_result(path)
    return findings


@pytest.mark.xfail(reason='failing magic/list parer')
def test_decider_headlines_master72_2_20(testdir, monkeypatch):
    source = tests.resources.MASTER72
    pages = '2:20'
    findings = decide_headline_style(
        source,
        pages,
        MASTER_72_DOCSTYLE,
        testdir,
        monkeypatch,
    )
    # no font size error
    assert not findings


@pytest.mark.xfail(reason='failing magic/list parer')
def test_decider_headlines_master72_all(testdir, monkeypatch):
    source = tests.resources.MASTER72
    pages = '3:65'
    findings = decide_headline_style(
        source,
        pages,
        MASTER_72_DOCSTYLE,
        testdir,
        monkeypatch,
    )
    # no font size error
    assert not findings


@pytest.mark.xfail(reason='failing magic/list parer')
def test_decider_headlines_bachelor76(testdir, monkeypatch):
    # TODO: EXTEND THIS TESTS, specify expected findings
    source = tests.resources.BACHELOR76
    pages = '4:67'
    findings = decide_headline_style(
        source,
        pages,
        BACHELOR_76_DOCSTYLE,
        testdir,
        monkeypatch,
    )
    # TODO: IMPROVE HEADLINE EXTRACTOR
    expected = 32  # not correct, but indicates that algo changed
    assert len(findings) == expected


def test_decider_headlines_chapter_on_new_page(testdir, monkeypatch):
    source = tests.resources.BACHELOR76
    pages = '0:42'
    findings = decide_headline_style(
        source,
        pages,
        NO_STYLE,
        testdir,
        monkeypatch,
    )
    no_new_page_start = protocol.select_findings(findings, 7540)
    assert len(no_new_page_start) == 2, str(no_new_page_start)

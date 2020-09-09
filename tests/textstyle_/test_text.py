# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw

import decider_textstyle.path
import tests.textstyle_

NO_STYLE = iamraw.DocTextStyle()


def decide_text_style(source, pages, style, testdir, monkeypatch):
    tests.textstyle_.write_docstyle(style, testdir.tmpdir)
    tests.textstyle_.run(
        f'--text -i {testdir.tmpdir} -i {source} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    path = decider_textstyle.path.text(testdir.tmpdir)
    findings = serializeraw.load_findings(path)
    return findings


@pytest.mark.xfail(reason='failing magic/list parser')
def test_decider_text_master72_2_20_fontsize(testdir, monkeypatch):
    style = iamraw.DocTextStyle(text_size=12.0)
    source = power.link(power.MASTER072_PDF)
    pages = '2:20'
    findings = decide_text_style(
        source,
        pages,
        style,
        testdir,
        monkeypatch,
    )
    assert not findings


def test_decider_text_master72_2_10_fontfamily(testdir, monkeypatch):
    # Hint: adjust text_family after text parser change
    style = iamraw.DocTextStyle(text_family=-1702503278)
    source = power.link(power.MASTER072_PDF)
    pages = '2:10'
    findings = decide_text_style(
        source,
        pages,
        style,
        testdir,
        monkeypatch,
    )
    # not correct, but indicates that algo changed
    assert len(findings) == 7


@pytest.mark.xfail(reason='failing magic/list parer')
def test_decider_text_bachelor76_4_10_bold_font(testdir, monkeypatch):
    source = power.link(power.BACHELOR076_PDF)
    pages = '2:10'
    findings = decide_text_style(
        source,
        pages,
        NO_STYLE,
        testdir,
        monkeypatch,
    )
    # five words marked bold
    assert len(findings) == 5


def test_decider_textstyle_merge_connected_findings(testdir, monkeypatch):
    """Merge more than one line with the same finding into a single
    finding."""
    source = power.link(power.MASTER072_PDF)
    tests.textstyle_.run(
        f'-i {source} --text --pages=18:22',
        monkeypatch=monkeypatch,
    )

    findings = serializeraw.load_findings(
        decider_textstyle.path.text(testdir.tmpdir),
        msgids=7550,
    )
    assert len(findings) == 1, len(findings)

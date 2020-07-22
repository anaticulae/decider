# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import doctextstyle.data
import protocol
import pytest

import decider_textstyle.path
import tests.resources
import tests.textstyle_

NO_STYLE = doctextstyle.data.DocTextStyle()


def decide_text_style(source, pages, style, testdir, monkeypatch):
    tests.textstyle_.write_docstyle(style, testdir.tmpdir)
    tests.textstyle_.run(
        f'--text -i {testdir.tmpdir} -i {source} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    path = decider_textstyle.path.text(testdir.tmpdir)
    findings = protocol.load_result(path)
    return findings


@pytest.mark.xfail(reason='failing magic/list parser')
def test_decider_text_master72_2_20_fontsize(testdir, monkeypatch):
    style = doctextstyle.data.DocTextStyle(text_size=12.0)
    source = tests.resources.MASTER72
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
    style = doctextstyle.data.DocTextStyle(text_family=-1702503278)
    source = tests.resources.MASTER72
    pages = '2:10'
    findings = decide_text_style(
        source,
        pages,
        style,
        testdir,
        monkeypatch,
    )
    # not correct, but indicates that algo changed
    assert len(findings) == 17


@pytest.mark.xfail(reason='failing magic/list parer')
def test_decider_text_bachelor76_4_10_bold_font(testdir, monkeypatch):
    source = tests.resources.BACHELOR76
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

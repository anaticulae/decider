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

import decider_textstyle.path
import tests.resources
import tests.textstyle_


def decide_text_style(source, pages, style, testdir, monkeypatch):
    tests.textstyle_.write_docstyle(style, testdir.tmpdir)
    tests.textstyle_.run(
        f'--text -i {testdir.tmpdir} -i {source} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    path = decider_textstyle.path.text(testdir.tmpdir)
    findings = protocol.load_result(path)
    return findings


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
    style = doctextstyle.data.DocTextStyle(text_family=873240484)
    source = tests.resources.MASTER72
    pages = '2:10'
    findings = decide_text_style(
        source,
        pages,
        style,
        testdir,
        monkeypatch,
    )
    assert len(findings) == 17

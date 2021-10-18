# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import iamraw.path
import power
import protocol
import pytest
import serializeraw
import utila
import utilatest

import decider_footnote.features.style
import decider_footnote.footnote
import decider_footnote.rules.start
import tests.footnote_


@pytest.fixture
def example():
    loaded = serializeraw.load_footnotes(
        power.link(power.MASTER072_PDF),
        pages=(3),
    )
    return loaded[0]


def test_footnotes_example(example):  # pylint:disable=W0621
    assert example.page == 3
    assert len(example.content) == 6


# def test_footnotes_validate(example):  # pylint:disable=W0621
#     result = [decider_footnote.footnote.validate(item) for item in example.content]

#     valid = [item.valid for item in result]

#     expected = [True, False, False, False, False, False]
#     assert valid == expected


def test_footnotes_most_common_font(example):  # pylint:disable=W0621
    data = example.content
    fontconfig = decider_footnote.footnote.most_common_font(data)
    collected = [item is not None for item in vars(fontconfig).values()]
    assert all(collected), fontconfig


def test_footnotes_most_common_font_empty():
    fontconfig = decider_footnote.footnote.most_common_font(items=[])
    assert fontconfig is None


@utilatest.longrun
def test_footnotes_work_highnote_rise(monkeypatch):
    footerheader = iamraw.path.headerfooters(power.link(power.MASTER072_PDF))
    fontheader = iamraw.path.fontheader(power.link(power.MASTER072_PDF))
    fontcontent = iamraw.path.fontcontent(power.link(power.MASTER072_PDF))
    with monkeypatch.context() as context:
        context.setattr(
            decider_footnote.features.style,
            'HIGHNOTE_RISE_DIFF_MAX',
            0.0,
        )
        user, _ = decider_footnote.features.style.work(
            footerheader,
            fontheader,
            fontcontent,
        )
    result = serializeraw.load_findings(user, 2003)
    assert len(result) == 260  # TODO: VERIFY LATER


def test_footnotes_work_highnote_size(monkeypatch):
    # TODO: LOOK FOR AN EXAMPLE WITH WRONG HIGHNOTE SIZE
    footerheader = iamraw.path.headerfooters(power.link(power.MASTER072_PDF))
    fontheader = iamraw.path.fontheader(power.link(power.MASTER072_PDF))
    fontcontent = iamraw.path.fontcontent(power.link(power.MASTER072_PDF))
    with monkeypatch.context() as context:
        context.setattr(
            decider_footnote.features.style,
            'HIGHNOTE_SIZE_DIFF_MAX',
            0.0,
        )
        user, _ = decider_footnote.features.style.work(
            footerheader,
            fontheader,
            fontcontent,
        )
    result = serializeraw.load_findings(user, 2004)
    assert not result


def test_footnotes_work_highnote_font_family():
    footerheader = iamraw.path.headerfooters(power.link(power.MASTER072_PDF))
    fontheader = iamraw.path.fontheader(power.link(power.MASTER072_PDF))
    fontcontent = iamraw.path.fontcontent(power.link(power.MASTER072_PDF))
    user, _ = decider_footnote.features.style.work(
        footerheader,
        fontheader,
        fontcontent,
    )
    result = serializeraw.load_findings(user, 2005)
    assert len(result) == 2


def test_footnote_email_exception(testdir, monkeypatch):
    source = power.link(power.HOME025_PDF)
    cmd = f'--rules -i {source}'

    def run_linter():
        tests.footnote_.run(cmd, monkeypatch=monkeypatch)
        loaded = utila.select_content(
            protocol.findings_from_path(testdir.tmpdir),
            page=0,
            default=[],
        )
        loaded = protocol.select_findings(loaded, {2001, 2002})
        return loaded

    with monkeypatch.context() as context:
        # disable exception to verify that this method is required
        context.setattr(
            decider_footnote.rules.start,
            'footnote_exception',
            lambda _: False,
        )
        loaded = run_linter()
        assert loaded

    loaded = run_linter()
    assert not loaded

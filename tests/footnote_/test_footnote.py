# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import iamraw.path
import protocol
import pytest

import decider_footnote.features.rules
import decider_footnote.features.style
import decider_footnote.footnote
import tests.resources


@pytest.fixture
def example():
    loaded = decider_footnote.footnote.load_frompath(
        tests.resources.MASTER72,
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


def test_footnotes_work_highnote_rise(monkeypatch):
    footerheader = iamraw.path.headerfooters(tests.resources.MASTER72)
    with monkeypatch.context() as context:
        context.setattr(
            decider_footnote.features.style,
            'MAX_HIGHNOTE_RISE_DIFF',
            0.0,
        )
        user, _ = decider_footnote.features.style.work(footerheader)
    result = tests.load_byid(user, 2003)
    assert len(result) == 255


def test_footnotes_work_highnote_size(monkeypatch):
    # TODO: LOOK FOR AN EXAMPLE WITH WRONG HIGHNOTE SIZE
    footerheader = iamraw.path.headerfooters(tests.resources.MASTER72)
    with monkeypatch.context() as context:
        context.setattr(
            decider_footnote.features.style,
            'MAX_HIGHNOTE_SIZE_DIFF',
            0.0,
        )
        user, _ = decider_footnote.features.style.work(footerheader)
    result = tests.load_byid(user, 2004)
    assert not result


def test_footnotes_work_highnote_font_family():
    footerheader = iamraw.path.headerfooters(tests.resources.MASTER72)
    user, _ = decider_footnote.features.style.work(footerheader)
    result = tests.load_byid(user, 2005)
    assert len(result) == 2

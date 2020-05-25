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

import decider_footnote.features.footnote
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


@contextlib.contextmanager
def active_ids(monkeypatch, ids=None):
    if ids is None:
        ids = []
    with monkeypatch.context() as context:
        parsed = protocol.parse_checkers(decider_footnote.features.footnote)
        for item in parsed:
            msgid = protocol.parse_msgid(item.__name__)
            if msgid in ids:
                item.confidence = 1.0
            else:
                item.confidence = 0.0
        yield context


def enable(items, active=None):
    if active is None:
        active = {}
    result = [
        protocol.MessageStatus(item, active=item in active) for item in items
    ]
    return result


def empty(result):
    return result == '[]\n'


def test_footnotes_work_disable_all(monkeypatch):
    footerheader = iamraw.path.headerfooters(tests.resources.MASTER72)
    with active_ids(monkeypatch, ids=[]):
        user, _ = decider_footnote.features.footnote.work(footerheader)
    assert empty(user), f'not all events are disabled:\n {user}'


def test_footnotes_work_highnote_rise(monkeypatch):
    footerheader = iamraw.path.headerfooters(tests.resources.MASTER72)
    with active_ids(
            monkeypatch,
            ids=[2003],
    ) as context:
        context.setattr(
            decider_footnote.features.footnote,
            'MAX_HIGHNOTE_RISE_DIFF',
            0.0,
        )
        user, _ = decider_footnote.features.footnote.work(footerheader)
    assert not empty(user)


def test_footnotes_work_highnote_size(monkeypatch):
    # TODO: LOOK FOR AN EXAMPLE WITH WRONG HIGHNOTE SIZE
    footerheader = iamraw.path.headerfooters(tests.resources.MASTER72)
    with active_ids(
            monkeypatch,
            ids=[2004],
    ) as context:
        context.setattr(
            decider_footnote.features.footnote,
            'MAX_HIGHNOTE_SIZE_DIFF',
            0.0,
        )
        user, _ = decider_footnote.features.footnote.work(footerheader)
    assert empty(user), user


def test_footnotes_work_highnote_font_family(monkeypatch):
    footerheader = iamraw.path.headerfooters(tests.resources.MASTER72)
    with active_ids(
            monkeypatch,
            ids=[2005],
    ):
        user, _ = decider_footnote.features.footnote.work(footerheader)
    assert not empty(user), 'no invalid font detection'

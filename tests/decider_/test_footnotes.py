# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import contextlib
import os

import hey.path
import protocol
import pytest
import utila

import decider.features.footnotes
import decider.footnotes
import tests.resources


@pytest.fixture
def example():
    loaded = decider.footnotes.load_frompath(
        tests.resources.MASTER72_GENERATED,
        pages=(3),
    )
    return loaded[0]


def test_decider_footnotes_example(example):  # pylint:disable=W0621
    assert example.page == 3
    assert len(example.content) == 6


def test_decider_footnotes_validate(example):  # pylint:disable=W0621
    result = [decider.footnotes.validate(item) for item in example.content]

    valid = [item.valid for item in result]

    expected = [True, False, False, False, False, False]
    assert valid == expected


def test_decider_cli_footnotes(testdir, monkeypatch):  ## pylint:disable=W0621
    root = str(testdir)

    cmd = ['-i', tests.resources.MASTER72_GENERATED, '-o', root]
    tests.run_decider(cmd, monkeypatch)

    outpath = os.path.join(root, 'decider__footnotes_user.yaml')
    assert os.path.exists(outpath), outpath

    dumped = utila.file_read(outpath)
    assert len(dumped) > 1000  # result contains some content
    assert '{%number%}' not in dumped, dumped  # ensure that template is replaced


def test_footnotes_most_common_font(example):  # pylint:disable=W0621
    data = example.content
    fontconfig = decider.footnotes.most_common_font(data)
    collected = [item is not None for item in vars(fontconfig).values()]
    assert all(collected), fontconfig


def test_footnotes_most_common_font_empty():
    fontconfig = decider.footnotes.most_common_font(items=[])
    assert fontconfig is None


@contextlib.contextmanager
def active_ids(monkeypatch, ids=None):
    if ids is None:
        ids = []
    with monkeypatch.context() as context:
        disable_all = enable(decider.features.footnotes.IDS, active=ids)
        context.setattr(decider.features.footnotes, 'MSG_STATUS', disable_all)
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
    footerheader = hey.path.headerfooters(tests.resources.MASTER72_GENERATED)
    with active_ids(monkeypatch, ids=[]):
        user, _ = decider.features.footnotes.work(footerheader)
    assert empty(user), f'not all events are disabled:\n {user}'


def test_footnotes_work_highnote_rise(monkeypatch):
    footerheader = hey.path.headerfooters(tests.resources.MASTER72_GENERATED)
    with active_ids(
            monkeypatch,
            ids=[decider.features.footnotes.INVALID_HIGHNOTE_RISE],
    ) as context:
        context.setattr(
            decider.features.footnotes,
            'MAX_HIGHNOTE_RISE_DIFF',
            0.0,
        )
        user, _ = decider.features.footnotes.work(footerheader)
    assert not empty(user)


def test_footnotes_work_highnote_size(monkeypatch):
    # TODO: LOOK FOR AN EXAMPLE WITH WRONG HIGHNOTE SIZE
    footerheader = hey.path.headerfooters(tests.resources.MASTER72_GENERATED)
    with active_ids(
            monkeypatch,
            ids=[decider.features.footnotes.INVALID_HIGHNOTE_SIZE],
    ) as context:
        context.setattr(
            decider.features.footnotes,
            'MAX_HIGHNOTE_SIZE_DIFF',
            0.0,
        )
        user, _ = decider.features.footnotes.work(footerheader)
    assert empty(user), user


def test_footnotes_work_highnote_font_family(monkeypatch):
    footerheader = hey.path.headerfooters(tests.resources.MASTER72_GENERATED)
    with active_ids(
            monkeypatch,
            ids=[decider.features.footnotes.INVALID_HIGHNOTE_FONT_FAMILY],
    ):
        user, _ = decider.features.footnotes.work(footerheader)
    assert not empty(user), 'no invalid font detection'

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw

import decider_toc.balance


@pytest.fixture
def master98_data():
    source = power.link(power.MASTER098_PDF)
    toc = serializeraw.load_toc(source)
    assert toc
    flat = decider_toc.balance.data(toc)
    return flat


@pytest.fixture
def master99_data():
    source = power.link(power.MASTER099_PDF)
    toc = serializeraw.load_toc(source)
    assert toc
    flat = decider_toc.balance.data(toc)
    return flat


@pytest.fixture
def master99_toc():
    source = power.link(power.MASTER099_PDF)
    toc = serializeraw.load_toc(source)
    return toc


def test_toc_section_balance():
    source = power.link(power.MASTER098_PDF)
    toc = serializeraw.load_toc(source)
    balance = decider_toc.balance.section_balance(toc)
    assert balance.level1
    assert balance.level2
    assert balance.level3 is None


def test_toc_master98_level_one(master98_data):  # pylint:disable=W0621
    level1 = decider_toc.balance.level_one(master98_data)
    assert level1 == [4, 20, 16, 25, 18, 3, 8, None]


def test_toc_master98_level_two(master98_data):  # pylint:disable=W0621
    level2 = decider_toc.balance.level_two(master98_data)
    expected = [
        [6, 6, 3, 5],
        [4, 4, 3, 5],
        [5, 0, 4, 16],
        [2, 2, 4, 1, 7, 2],
        [7, 1],
    ]
    assert level2 == expected


def test_toc_master99_level_one(master99_data):  # pylint:disable=W0621
    level1 = decider_toc.balance.level_one(master99_data)
    assert level1 == [1, 3, 11, 12, 14, 2, 9, 23, 5, 5, 1, 8, None]


def test_toc_master99_level_two(master99_data):  # pylint:disable=W0621
    level2 = decider_toc.balance.level_two(master99_data)
    expected = [[0, 1, 0, 2], [3, 8], [8, 5], [4, 1, 1, 1, 2], [1, 2, 5, 15]]
    assert level2 == expected


def test_toc_master99_level_three(master99_data):  # pylint:disable=W0621
    level3 = decider_toc.balance.level_three(master99_data)
    expected = [[4, 3], [3, 1], [11, 3]]
    assert level3 == expected


def test_toc_judge(master99_toc):  # pylint:disable=W0621
    judged = decider_toc.balance.judge(master99_toc)
    expected = decider_toc.balance.JudgedBalance(
        level1=None,
        level2=[[(0,), (0,), (0,), (0,)], [(0,), (1, 8, 5.9)],
                [(1, 8, 5.9), (0,)], [(0,), (0,), (0,), (0,), (0,)],
                [(0,), (0,), (0,), (1, 15, 5.9)]],
        level3=[[(0,), (0,)], [(0,), (0,)], [(1, 11, 6.5), (0,)]])
    assert expected == judged

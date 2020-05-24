# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import statistics
import typing

import iamraw
import utila

import decider_toc.utils

TocLine = collections.namedtuple('TocLine', 'page level title')
TocLines = typing.List[TocLine]

Evaluated = collections.namedtuple(
    'Evaluated',
    'min, max, mean, median, variance, stdev',
)

Balance = collections.namedtuple('Balance', 'level1, level2, level3')
Level = collections.namedtuple('Level', 'level1, level2, level3')

JudgedBalance = collections.namedtuple(
    'JudgedBalance',
    'level1, level2, level3',
)

# TODO: MOVE CONSTANT TO IAMRAW
LEVEL_ONE = 1
LEVEL_TWO = 2
LEVEL_THREE = 3


def judge(toc: iamraw.Toc) -> JudgedBalance:
    balance = section_balance(toc)
    levels = level(toc, flat=False)

    level1_validated = None  # TODO: LEVEL 1 JUDGEMENT
    level2_validated = validate_level(levels.level2, balance.level2)
    level3_validated = validate_level(levels.level3, balance.level3)

    result = JudgedBalance(
        level1=level1_validated,
        level2=level2_validated,
        level3=level3_validated,
    )
    return result


def validate_level(items: list, balance: Evaluated) -> list:
    """Decide if size of sections is too high(1), too small(-1) or in
    range(0).

    Args:
        items: list of groups of section length
        balance(Evaluated): global text style
    Returns:
        list of group with judged result
    """
    result = []
    for group in items:
        stepresult = []
        for item in group:
            upper = balance.median + balance.stdev
            lower = balance.median - balance.stdev
            if item > upper:
                stepresult.append(1)
            elif item < lower:
                stepresult.append(-1)
            else:
                stepresult.append(0)
        result.append(stepresult)
    return result


def section_balance(toc: iamraw.Toc) -> Balance:
    level1_flat, level2_flat, level3_flat = level(toc)

    balance1 = analyse(level1_flat)
    balance2 = analyse(level2_flat)
    balance3 = analyse(level3_flat)

    return Balance(balance1, balance2, balance3)


def level(toc: iamraw.Toc, flat: bool = True) -> Level:
    extracted = data(toc)

    level1 = [item for item in level_one(extracted) if item is not None]

    level2 = level_two(extracted)
    level2_flat = utila.flatten(level2)

    level3 = level_three(extracted)
    level3_flat = utila.flatten(level3)

    if flat:
        return Level(level1, level2_flat, level3_flat)
    return Level(level1, level2, level3)


def data(toc: iamraw.Toc) -> TocLines:
    flat = decider_toc.utils.flat(toc)
    result = []
    for item in flat:
        result.append(TocLine(int(item.page), item.level, item.title))
    return result


def analyse(items: list) -> Evaluated:
    if not items:
        return None

    mean = statistics.mean(items)
    variance = statistics.variance(items)
    stdev = statistics.stdev(items)
    median = statistics.median(items)
    max_ = max(items)
    min_ = min(items)

    mean, variance, stdev, median, max_, min_ = utila.roundme(
        mean,
        variance,
        stdev,
        median,
        max_,
        min_,
        digits=4,
    )

    result = Evaluated(
        min=min_,
        max=max_,
        mean=mean,
        median=median,
        variance=variance,
        stdev=stdev,
    )
    return result


def level_one(items) -> utila.Numbers:
    pages = [item[0] for item in items if item[1] == LEVEL_ONE]
    result = []
    for current, after in zip(pages[0:-1], pages[1:]):
        result.append(after - current)
    # require document page count to determine length of last `level one`
    # section.
    result.append(None)
    return result


def level_two(items):
    # TODO: DECIDE CASE WHERE LEVEL TWO IS THE LAST ITEM AND THEREFORE A
    # FOLLOWING LINE MISSING.
    result = []
    items = [(item[0], item[1])
             for item in items
             if item[1] in (LEVEL_ONE, LEVEL_TWO)]
    group = []
    for current, after in zip(items[0:-1], items[1:]):
        if current[1] == LEVEL_ONE:
            continue
        group.append(after[0] - current[0])
        if after[1] == LEVEL_ONE and group:
            result.append(group)
            group = []
    if group:
        result.append(group)
    return result


def level_three(items):
    # TODO: DECIDE CASE WHERE LEVEL TWO IS THE LAST ITEM AND THEREFORE A
    # FOLLOWING LINE MISSING.
    result = []
    items = [(item[0], item[1])
             for item in items
             if item[1] in (LEVEL_ONE, LEVEL_TWO, LEVEL_THREE)]
    group = []
    for current, after in zip(items[0:-1], items[1:]):
        if current[1] in (LEVEL_ONE, LEVEL_TWO):
            continue
        group.append(after[0] - current[0])
        if after[1] in (LEVEL_ONE, LEVEL_TWO) and group:
            result.append(group)
            group = []
    if group:
        result.append(group)
    return result


def split_bysection(items):
    if not items:
        return []
    result = [[items[0]]]
    for item in items[1:]:
        if result[-1][-1][1] == item[1]:
            result[-1].append(item)
        else:
            result.append([item])
    return result

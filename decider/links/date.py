# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


def mixed(date) -> bool:
    """\
    >>> mixed([18, 10, 10])
    True
    >>> mixed([2018, 10, 10])
    False
    """
    values = [int(item) for item in date]
    return max(values) <= 1800


MIN_MIXED_RATE = 0.6


def is_mixed(dates):
    if len(dates) <= 5:
        return False
    mixes = [date for date in dates if mixed(date)]
    rate = len(mixes) / len(dates)
    if rate >= MIN_MIXED_RATE:
        return True
    return False

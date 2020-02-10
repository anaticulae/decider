# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""left right border detector
==========================

The `left right border detector` (lrbd) separates borders of the left
and right page especially which are used for books with different border
width for left and right page.

As a result of different left-right borders there are alternating border
widths which we detect. On single pages there are no alternating border.

Some documents have exceptions on some pages. We handle this via allowed
errors defined with the HolyValues `MAX_FIRSTSECOND_ERROR` and
`MIN_MIXED_ERROR`.

TODO: MOVE TO HEY PACKAGE LATER
"""

import dataclasses
import typing

import configo
import iamraw
import utila

import border.detection.most
import border.utils

# max diff to match in common group.
MAX_SIDE_DIFF = configo.HV_INT_PLUS(default=2.0)
# exceptions which are allowed cause of user defined error.
MAX_FIRSTSECOND_ERROR = configo.HV_PERCENT_PLUS(default=5)
# errors which are a result of handle alternating border as single border.
MIN_MIXED_ERROR = configo.HV_PERCENT_PLUS(default=15)
# area where left border can be located.
LEFT_PERCENT = configo.HV_PERCENT_PLUS(default=30)
# area where right border can be located.
RIGHT_PERCENT = configo.HV_PERCENT_PLUS(default=30)

LeftRight = typing.Tuple[float, float]


@dataclasses.dataclass
class LeftRightDetected:
    # TODO: SUPPORT FLOAT AND TUPLE OF FLOAT
    left: tuple = None
    right: tuple = None
    confidence: float = 0.0

    @property
    def valid(self):
        return isinstance(self.left, tuple)


def run(  # pylint:disable=too-many-locals
        textpositions: iamraw.PageContentTextPositions,
        pagesizes: iamraw.PageSizeBorderList,
) -> LeftRightDetected:
    """Run LeftRight-Stategy to determine that document contains special
    leftright-border or a normal equal border for every page."""
    assert len(textpositions) == len(pagesizes), 'could not sync iterator'

    left = []
    right = []
    for page, size in zip(textpositions, pagesizes):
        # remove index
        leftright = maximize_leftright(page.content.values(), size)
        left.append(leftright[0])
        right.append(leftright[1])

    mixed = border.utils.diff_mode(left, max_diff=MAX_SIDE_DIFF.value)
    # first side
    first = left[::2]
    first_matched = border.utils.diff_mode(first, max_diff=MAX_SIDE_DIFF.value)
    # second side
    second = left[1::2]
    second_matched = border.utils.diff_mode(second, max_diff=MAX_SIDE_DIFF.value) # yapf:disable

    mixed_error = 1 - len(mixed) / len(left)
    first_error = 1 - len(first_matched) / len(first)
    second_error = 1 - len(second_matched) / len(second)

    utila.debug(f'mixed: {mixed_error}')
    utila.debug(f'first: {first_error}')
    utila.debug(f'second: {second_error}')

    # left right
    # TODO: DEFINE BETTER CONFIDENCE APPROACH
    if mixed_error > MIN_MIXED_ERROR.value and all([
            first_error < MAX_FIRSTSECOND_ERROR.value,
            second_error < MAX_FIRSTSECOND_ERROR.value,
    ]):
        leftborder = (
            border.utils.multi_mode(first),
            border.utils.multi_mode(second),
        )
        rightborder = (
            border.utils.multi_mode(right[::2], minimize=False),
            border.utils.multi_mode(right[1::2], minimize=False),
        )
        return LeftRightDetected(
            left=leftborder,
            right=rightborder,
            confidence=1.0,
        )
    leftborder = border.utils.multi_mode(left)
    rightborder = border.utils.multi_mode(right, minimize=False)
    return LeftRightDetected(
        left=leftborder,
        right=rightborder,
        confidence=1.0,
    )


def maximize_leftright(
        boundings: border.data.Rectangles,
        size: iamraw.PageSizeBorder,
) -> LeftRight:
    """Determine the left and right border of a page based on `mode`
    selection in `size`.

    Minimize the left and maximize the right position. The area where
    mode is used to determine the most common border which is assumed as
    correct border is limit by `size` configuration.

    Args:
        boundings: textpositions of defined page
        size: width and height of current page
    Returns:
        tuple with left and right content bounding
    """
    left_max = size.size.width * LEFT_PERCENT.value
    right_min = size.size.width * (1 - RIGHT_PERCENT.value)
    # TODO: REPLACE AFTER UPGRADING UTILA
    left_max, right_min = utila.roundme(left_max), utila.roundme(right_min)
    assert left_max <= right_min, 'left and right bounds are flipped'

    left = [item[0] for item in boundings if item[0] <= left_max]
    right = [item[2] for item in boundings if item[2] >= right_min]

    left = border.utils.multi_mode(left)
    right = border.utils.multi_mode(right, minimize=False)
    return left, right

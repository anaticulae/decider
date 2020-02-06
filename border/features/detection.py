# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""common border validator
=======================
Detect the common border of selected `pages` as a expected correct page
border. Validate every page against this common border. Keep in mind to
decide between left and right page. In some printings there are two
different border **We do not support them yet**.

Some pdf-writer produces a massive amout of empty strings as a result of
miss-using `what you see is what you get`-editors. In some cases there
are a lot of `hit the box` errors.

* TODO: SUPPORT DIFFERENT LEFT AND RIGHT PAGE
* TODO: MARK EMPTY STRING LAYOUT ERRORS.
"""

import math
import typing

import serializeraw
import utila

Rectangle = typing.Tuple[float, float, float, float]
Rectangles = typing.List[Rectangle]


def work(border_boxes: str, border_pages: str, pages: tuple = None) -> str:
    utila.call('work: border detection')
    boxes = serializeraw.load_boundingboxes(border_boxes, pages=pages)
    sizeandborder = serializeraw.load_pageborders(border_pages, pages=pages)

    border = most_boundingbox([item.border for item in sizeandborder])
    utila.info(f'{border}')

    def boxprovider(page: int):  # pylint:disable=unused-argument
        # TODO: Differentiate between left and right side
        return border

    hits = boxes_outside_border(boxes, boxprovider)
    utila.debug(hits)

    dumped = serializeraw.dump_hits(border, hits)
    return dumped


def boxes_outside_border(boxes, border: callable):
    """Determine `boxes` which are outside out of `border`."""
    result = []
    # x0 y0 x1 y1
    for page in boxes:
        border_box = border(page.page)
        for index, bounding in page.boundings:
            # BOUNDING:     'left, top,  right, bottom'
            # BORDER:       'left  right top    bottom'

            # move bounding to center of page to make approach more robust
            rounded_bounding = round_bounding(bounding)
            if not any([
                    rounded_bounding[0] < border_box[0],
                    rounded_bounding[2] > border_box[1],
                    rounded_bounding[1] < border_box[2],
                    rounded_bounding[3] > border_box[3],
            ]):
                # all items in the box
                continue
            result.append((page.page, index, bounding))
    return result


def round_bounding(item: Rectangle) -> Rectangle:
    """Round border in direction to the center of the rectangle to get a
    `smaller` rectangle which fit in more parent rectangles."""
    # round to move coordinate in center direction of page
    rounding = [
        math.ceil,  # x0
        math.ceil,  # y0
        math.floor,  # x1
        math.floor,  # y1
    ]
    result = [method(item[index]) for index, method in enumerate(rounding)]
    return tuple(result)


def most_boundingbox(boxes: Rectangles, roundme: bool = False) -> Rectangle:
    """Extract bounding box of most common occurence for every side.

    Round detected boundingbox to full number to make approach more
    robust. Round numbers in direction to the border end to increase the
    detected rectangle that fit more items in it.
    """
    # TODO: Think about right and left, maybe search for the top 2 borders?
    # Filter None entries
    rounding = [math.floor, math.floor, math.ceil, math.ceil]
    result = []
    for index, method in enumerate(rounding):
        # remove None items
        filtered = [item[index] for item in boxes if item[index] is not None]
        # round to have a more robust grouping
        rounded = [method(item) for item in filtered] if roundme else filtered
        # determine most occured border to determine them as required border
        mode = statistics.mode(rounded)
        result.append(mode)
    # (x0, y0, x1, y1)
    return tuple(result)

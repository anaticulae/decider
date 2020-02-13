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

import functools
import math
import typing

import iamraw
import protocol
import serializeraw
import utila

import border.data
import border.detection
import border.detection.most
import border.utils
import decider.utils


def work(
        border_boxes: str,
        border_pages: str,
        textpositions: str,
        pages: tuple = None,
) -> typing.Tuple[str, str, str]:
    utila.call('work: border detection')
    boxes = serializeraw.load_boundingboxes(border_boxes, pages=pages)
    sizeandborder = serializeraw.load_pageborders(border_pages, pages=pages)
    textpositions = serializeraw.load_textpositions(textpositions, pages=pages)

    expected = border.detection.determine_border(textpositions, sizeandborder)

    hits = boxes_outside_border(boxes, expected)
    utila.debug(hits)

    dumped = serializeraw.dump_hits(hits)

    linter = decider.utils.from_module(__name__)
    linting(hits, linter)

    user, developer = protocol.dump_result(linter.result, unique=True)
    return dumped, user, developer


def linting(
        hits,
        linter: protocol.Linter,
):
    checkers = decider.utils.parse_checkers(__name__)
    for checker in checkers:
        for page in hits:
            location = protocol.Location.from_page(page.page)
            call = functools.partial(
                linter.add_finding,
                msgid=checker.msgid,
                location=location,
            )
            for hit in page.hits:
                checker(call, hit)


# TODO: ADD DIFFERENT BORDER CHECKER LINTER FOR DIFFRENT AREAS, footenote,
# pagecontent, cropbox, etc.

SOLUTION_2020 = """\
Objekt beschreibt Seitenrand

Passen Sie die Formatierung an, so dass der Inhalt nicht mehr in den
Seitenrad ragt.
"""


def check_2020_content_inside_box(linter, item):  # pylint:disable=W0613
    """Ensure that content fits in detected content box."""
    linter()


def boxes_outside_border(
        boxes,
        expected_border: callable,
) -> iamraw.PageContentHits:
    """Determine `boxes` which are outside out of `border`."""
    result = []
    # x0 y0 x1 y1
    for page in boxes:
        hits = []
        border_box = expected_border(page.page)
        for index, bounding in page.boundings:
            # BOUNDING:     'left, top,   right, bottom'
            # BORDER:       'left, right, top,   bottom'

            # move bounding to center of page to make approach more robust
            rounded_bounding = round_small(bounding)
            if not any([
                    rounded_bounding[0] < border_box[0],
                    rounded_bounding[2] > border_box[1],
                    rounded_bounding[1] < border_box[2],
                    rounded_bounding[3] > border_box[3],
            ]):
                # all items in the box
                continue
            hits.append((index, bounding))
        result.append(
            iamraw.PageContentHit(
                border=border_box,
                hits=hits,
                page=page.page,
            ))
    return result


def round_small(item: border.data.Rectangle) -> border.data.Rectangle:
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

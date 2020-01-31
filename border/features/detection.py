# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import statistics
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

    hits = hit_the_box(boxes, boxprovider)
    utila.debug(hits)

    dumped = serializeraw.dump_hits(border, hits)
    return dumped


def hit_the_box(boxes, border: callable):
    failures = []
    # x0 y0 x1 y1
    for page in boxes:
        pagenumber = page.page
        border_box = border(page.boundings)
        for index, bounding in page.boundings:
            # BOUNDING:     'left, top,  right, bottom'
            # BORDER:       'left  right top    bottom'
            if bounding[0] < border_box[0] or\
               bounding[2] > border_box[1] or\
               bounding[1] < border_box[2] or\
               bounding[3] > border_box[3]:
                failures.append((pagenumber, index, bounding))
    return failures


def most_boundingbox(boxes: Rectangles) -> Rectangle:
    """Extract bounding box of most common occurence for every side"""
    # TODO: Think about right and left, maybe search for the top 2 borders?
    # Filter None entries

    x0 = statistics.median([item[0] for item in boxes if item[0] is not None])
    y0 = statistics.median([item[1] for item in boxes if item[1] is not None])
    x1 = statistics.median([item[2] for item in boxes if item[2] is not None])
    y1 = statistics.median([item[3] for item in boxes if item[3] is not None])

    result = (x0, y0, x1, y1)
    return result

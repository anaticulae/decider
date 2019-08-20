# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from statistics import median
from typing import List
from typing import Tuple

from serializeraw import dump_hits
from serializeraw import load_boundingboxes
from serializeraw import load_pageborders
from utila import Flag
from utila import call
from utila import debug
from utila import info


def work(border_boxes: str, border_pages: str) -> str:
    call('work: border detection')
    boxes = load_boundingboxes(border_boxes)
    sizeandborder = load_pageborders(border_pages)

    border = most_boundingbox([item.border for item in sizeandborder])

    info('%s' % str(border))

    def boxprovider(page: int):  # pylint:disable=unused-argument
        # TODO: Differentiate between left and right side
        return border

    hits = hit_the_box(boxes, boxprovider)
    debug(hits)

    dumped = dump_hits(border, hits)
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


def most_boundingbox(boundingboxes: List[Tuple[float]]) -> Tuple[float]:
    """Extract bounding box of most common occurence for every side"""
    # TODO: Think about right and left, maybe search for the top 2 borders?

    # Filter None entries
    x0 = median([item[0] for item in boundingboxes if item[0]])
    y0 = median([item[1] for item in boundingboxes if item[1]])
    x1 = median([item[2] for item in boundingboxes if item[2]])
    y1 = median([item[3] for item in boundingboxes if item[3]])

    result = (x0, y0, x1, y1)
    return result


def name():
    return 'hitthebox'


def commandline():
    return Flag(longcut=name(), message='Extract border for every page')

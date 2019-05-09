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

from serializeraw import load_boundingboxes
from utila import Flag
from yaml import dump


def work(path: str) -> str:
    boxes = load_boundingboxes(path)

    border = most_boundingbox(boxes)

    def boxprovider(page: int):  # pylint:disable=unused-argument
        # TODO: Differentiate between left and right side
        return border

    hits = hit_the_box(boxes, boxprovider)

    dumped = dump(hits)
    return dumped


def hit_the_box(boxes, border: callable):
    failures = []
    for page, box in enumerate(boxes):
        border_box = border(page)
        if box[0] < border_box[0] or box[1] < border_box[1] or\
           box[2] > border_box[2] or box[3] > border_box[3]:
            failures.append(page, box)
    return failures


def most_boundingbox(boundingboxes: List[Tuple[float]]) -> Tuple[float]:
    # TODO: Think about right and left, maybe search for the top 2 borders?

    x0 = median([item[0] for item in boundingboxes])
    y0 = median([item[1] for item in boundingboxes])
    x1 = median([item[2] for item in boundingboxes])
    y1 = median([item[3] for item in boundingboxes])

    result = (x0, y0, x1, y1)
    return result


def name():
    return 'hitthebox'


def commandline():
    return Flag(longcut=name(), message='Extract border for every page')

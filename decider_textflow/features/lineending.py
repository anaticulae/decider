# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import protocol
import textflow.features.lineending


def work(lineendings: str, pages: tuple = None) -> protocol.ResultType:
    # TODO: REMOVE PYLINT LATER
    endings = textflow.features.lineending.load_lineendings(  # pylint:disable=E1123
        lineendings,
        pages=pages,
    )
    result = protocol.run(__name__, driver=endings)
    return result


SOLUTION_7000 = """\
Zu viele aufeinander folgende Trennungen

Es wird empfohlen die Anzahl der aufeinander folgenden Zeilen die eine \
Trennung enthalten auf 3 zu beschränken.

{darstellung/schriftbild#trennungen}
"""

FOLLOWING_DIVISION_MAX = 3


def check_7000_more_than_three_division(linter: callable, lineendings: list):
    """Ensure that there are not more than three following line
    divisions(-)."""

    def more_than_three(items):
        if not items:
            return []
        collected = [[items[0]]]
        for item in items[1:]:
            if collected[-1][-1][0] == '-' and item[0] == '-':
                collected[-1].append(item)
            else:
                collected.append([item])
        result = [
            item for item in collected if len(item) > FOLLOWING_DIVISION_MAX
        ]
        return result

    def merge_bounding(items):
        """Create bounding box around the list of division `-`. Limit
        the box to the left side, cause boundingbox is used from whole
        line but we want to highlight the last character."""
        boundings = [item[1] for item in items]
        x0, y0, x1, y1 = boundings[0]
        x0 = x1 - 20  # limit bounding box to 20 width
        for x00, y00, x11, y11 in boundings[1:]:
            # center box
            x00 = x11 - 20
            x11 = x11 + 20
            x0 = min([x0, x00])
            x1 = max([x1, x11])
            y0 = min([y0, y00])
            y1 = max([y1, y11])
        return (x0, y0, x1, y1)

    for page in lineendings:
        number = page.page
        failures = more_than_three(page.content)
        for failure in failures:
            bounding = merge_bounding(failure)
            location = iamraw.BoundingLocation.fromtuple(
                bounding=bounding,
                page=number,
            )
            linter(location=location)

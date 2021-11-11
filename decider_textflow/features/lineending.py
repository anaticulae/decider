# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import protocol
import serializeraw
import textflow.features.lineending


def work(
    lineendings: str,
    sentences: str,
    pages: tuple = None,
) -> protocol.ResultType:
    driver = create_driver(
        lineendings=lineendings,
        sentences=sentences,
        pages=pages,
    )
    result = protocol.run(
        __name__,
        driver=driver,
    )
    return result


SOLUTION_7000 = """\
Zu viele aufeinander folgende Trennungen

Es wird empfohlen die Anzahl der aufeinander folgenden Zeilen die eine \
Trennung enthalten auf 3 zu beschränken.

{darstellung/schriftbild#trennungen}
"""

FOLLOWING_DIVISION_MAX = configo.HV_INT_PLUS(default=3)


def check_7000_more_than_three_division(linter: callable, driver):
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

    for page in driver.lineendings:
        number = page.page
        failures = more_than_three(page.content)
        for failure in failures:
            bounding = merge_bounding(failure)
            location = iamraw.BoundingLocation.fromtuple(
                bounding=bounding,
                page=number,
            )
            linter(location=location)


def create_driver(lineendings, sentences, pages: tuple = None):
    # TODO: REMOVE PYLINT LATER
    lineendings = textflow.features.lineending.load_lineendings(  # pylint:disable=E1123
        lineendings,
        pages=pages,
    )
    sentences = serializeraw.load_text(
        sentences,
        pages=pages,
    )
    result = protocol.driver(
        lineendings=lineendings,
        sentences=sentences,
    )
    return result

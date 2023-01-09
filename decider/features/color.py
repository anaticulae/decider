# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import protocol
import serializeraw
import utila


def work(statistics: str, pages: tuple = None) -> protocol.ResultType:
    driver = create_driver(
        statistics,
        pages=pages,
    )
    result = protocol.run(
        __name__,
        driver=driver,
    )
    return result


def create_driver(statistics: str, pages: tuple = None):
    statistics = serializeraw.load_color_statistics(
        statistics,
        pages=pages,
    ) if utila.exists(statistics) else []
    result = protocol.driver(statistics=statistics)
    return result


SOLUTION_E10600 = """\
Grelle Farben

Überprüfen Sie die verwendete Farbe: {{color}}.
"""


def check_10600_bright_colors(linter, driver):
    for page in driver.statistics:
        for color, count in page.content:
            if count < COLOR_INVALID_COUNT_MIN:
                continue
            if not invalid_color(*color):
                continue
            color = utila.from_tuple(color)
            linter(
                color=color,
                location=iamraw.Location.from_page(page.page),
            )


COLOR_INVALID_COUNT_MIN = configo.HV_INT_PLUS(default=100 * 100)

# TODO: USE SMARTER COLOR CHECKER
INVALID = {
    utila.rgb2int(*item) for item in (
        (0, 0, 255),
        (0, 255, 0),
        (0, 255, 255),
        (128, 0, 256),
        (128, 255, 0),
        (128, 255, 128),
        (255, 0, 0),
        (255, 0, 128),
        (255, 0, 255),
        (255, 128, 128),
        (255, 128, 256),
        (255, 255, 0),
        (0, 176, 240),
    )
}


def invalid_color(red, green, blue) -> bool:
    color = utila.rgb2int(red, green, blue)
    if color in INVALID:
        return True
    return False

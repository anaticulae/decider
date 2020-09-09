# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import magic.data
import serializeraw
import utila

import decider_textflow.features


def work(
        headlines: str,
        text: str,
        textpositions: str,
        sizeandborders: str,
        headerfooter: str,
        textstyle: str,
        magiccontent: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    textstyle = serializeraw.load_doctextstyle(textstyle)
    magiccontent = magic.data.load_types(magiccontent, pages=pages)
    driver = decider_textflow.features.textdata(
        headlines,
        text,
        textpositions,
        sizeandborders,
        headerfooter,
        magiccontent=magiccontent,
        textstyle=textstyle,
        pages=pages,
    )
    result = decider_textflow.features.linting(__name__, driver)
    return result


SOLUTION_7630 = """\
Paragraph zu kurz

Der Abschnitt umfasst nur {%lines%} Zeilen und sollte überarbeitet werden.

TODO: ARTICLE
"""

PARAGRAPH_TOO_SHORT = 3


def check_7630_paragraph_too_short(linter: callable, driver):
    textstyle = driver.doctextstyle

    if textstyle.text_alignment == 0:
        # not justified
        return

    min_textwidth = textstyle.text_width - 35  # TODO: HOLY VALUE

    collected = []
    for page, line, item in driver.text_chunks:
        # TODO: USE VISITOR PATTERN
        if isinstance(item, iamraw.PageList):
            # TODO: THINK ABOUT WHAT WE CAN CHECK
            # no check before list starts.
            collected = []
            continue

        if isinstance(item, iamraw.Headline):
            too_short = 2 <= len(collected) <= PARAGRAPH_TOO_SHORT
            if too_short:
                location = ranged_location(collected)
                linter(location=location, lines=len(collected))
            collected = []
            continue
        if item is None:
            collected = []
            continue
        line_width = width(item)
        if line_width <= min_textwidth:
            collected.append((page, line, item))
            too_short = 2 <= len(collected) <= PARAGRAPH_TOO_SHORT
            if too_short:
                location = ranged_location(collected)
                linter(location=location, lines=len(collected))
            collected = []
        else:
            collected.append((page, line, item))


def ranged_location(collected) -> iamraw.RangedLocation:
    location = iamraw.RangedLocation(
        page=collected[0][0],
        page_end=collected[-1][0],
        line=collected[0][1],
        line_end=collected[-1][1],
    )
    return location


def width(item):
    bounding = item.bounding
    return utila.roundme(bounding.x1 - bounding.x0)

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import doctextstyle.serialize
import iamraw
import protocol
import utila

import decider_textflow.features


def work(  # pylint:disable=R0914
        headlines: str,
        text: str,
        textpositions: str,
        sizeandborders: str,
        headerfooter: str,
        textstyle: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    textstyle = doctextstyle.serialize.load_docstyle(textstyle)
    driver = decider_textflow.features.textdata(
        headlines,
        text,
        textpositions,
        sizeandborders,
        headerfooter,
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
        if isinstance(item, iamraw.Headline):
            too_short = 2 <= len(collected) <= PARAGRAPH_TOO_SHORT
            if too_short:
                location = protocol.RangedLocation(
                    page=collected[0][0],
                    page_end=collected[-1][0],
                    line=collected[0][1],
                    line_end=collected[-1][1],
                )
                linter(
                    location=location,
                    lines=len(collected),
                )
            collected = []
            continue
        line_width = width(item)
        if line_width <= min_textwidth:
            collected.append((page, line, item))
            too_short = 2 <= len(collected) <= PARAGRAPH_TOO_SHORT
            if too_short:
                location = protocol.RangedLocation(
                    page=collected[0][0],
                    page_end=collected[-1][0],
                    line=collected[0][1],
                    line_end=collected[-1][1],
                )
                linter(
                    location=location,
                    lines=len(collected),
                )
            collected = []
        else:
            collected.append((page, line, item))


def width(item):
    bounding = item.bounding
    return utila.roundme(bounding.x1 - bounding.x0)

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
Hurenkind: Single Line at Page Start
Schusterjunge: Single Line at Page End
"""

import typing

import iamraw
import protocol
import utila

import decider_textflow.features
import decider_textstyle.utils


def work(  # pylint:disable=R0914
        headlines: str,
        text: str,
        textpositions: str,
        sizeandborders: str,
        headerfooter: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    driver = decider_textflow.features.textdata(
        headlines,
        text,
        textpositions,
        sizeandborders,
        headerfooter,
        pages=pages,
    )
    result = decider_textflow.features.linting(__name__, driver)
    return result


SOLUTION_7620 = """\
Hurenkind: Einsame Zeile am Seitenanfang

Seite beginnt mit einsamer Zeile.

TODO: ARTICLE
"""


def check_7620_lonely_page_start(linter: callable, driver):
    linewidth = textwidth(driver.text_chunks)
    hurenkind_maxwidth = linewidth * 0.9  # TODO: HOLY VALUE
    text = decider_textstyle.utils.page_chunks(driver.text_chunks)
    for page, content in text:
        if len(content) < 2:
            continue
        first_headline = isinstance(content[0], iamraw.Headline)
        second_headline = isinstance(content[1], iamraw.Headline)

        if first_headline and second_headline:
            continue

        if second_headline and not first_headline:
            # hurenkind
            # TEXT -> HEADLINE
            location = protocol.RangedLocation(page=page, line=0)
            linter(location)
            continue

        if not first_headline and not second_headline:
            first_width = width(content[0])
            second_width = width(content[1])
            # TODO: HOLY VALUE
            second_full_line = utila.near(second_width, linewidth, diff=5.0)
            if first_width <= hurenkind_maxwidth and second_full_line:
                # hurenkind
                # SHORT TEXT -> TEXT
                location = protocol.RangedLocation(page=page, line=0)
                linter(location)
                continue


SOLUTION_7621 = """\
Schusterjunge: Einsame Zeile am Seitenende

"""


def textwidth(chunks) -> float:
    result = []
    for _, __, item in chunks:
        if isinstance(item, iamraw.Headline):
            continue
        result.append(width(item))

    result = utila.mode(result)
    return result


def width(item):
    bounding = item.bounding
    return utila.roundme(bounding.x1 - bounding.x0)

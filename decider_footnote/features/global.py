# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
""".. _decider_features_footnote:

Footnotes
=========
"""

import configos
import protoerror
import serializeraw
import utilo


def work(footerheader: str, pages: tuple = None) -> protoerror.ResultType:
    driver = create_driver(
        footerheader=footerheader,
        pages=pages,
    )
    result = protoerror.run(
        __name__,
        driver=driver,
    )
    return result


def create_driver(footerheader: str, pages: tuple = None):
    headerfooters = serializeraw.load_footnotes(footerheader, pages=pages)
    footnotes = []
    for page in headerfooters:
        for item in page.content:
            footnotes.append((page.page, item))
    result = protoerror.driver(footnotes=footnotes)
    return result


SOLUTION_2015 = """\
Endnoten verwendet

Im Dokument werden Endnoten verwendet. Ersetzen Sie diese durch \
stringend aufsteigende Fußnoten.

TODO: ARTICLE ENDNOTE_VS_FOOTNOTE
"""
# TODO: move MIN_CHECK to a decorator?
# require more than `15` footnote to run this linter
ENDNOTE_CHECK_NUMBER_MIN = configos.HV_INT_PLUS(default=15)

# Decide between endnotes and failing footnotes
STARTING_MIN = configos.HV_INT_PLUS(default=3)

STARTING_RATE_MIN = configos.HV_PERCENT_PLUS(default=80)


def check_2015_endnotes_using(linter, driver):
    numbers = [
        item.number
        for _, item in driver.footnotes
        if isinstance(item.number, int)
    ]
    if len(numbers) < ENDNOTE_CHECK_NUMBER_MIN:
        return
    # remove part of footnote without number
    numbers = [item for item in numbers if item != -1]
    if utilo.isascending(numbers):
        return
    grouped = utilo.groupby_ascending(numbers)
    # TODO : USE CHAINSAW DETECTOR HERE
    started = [item for item in grouped if starting(item)]
    rate = len(started) / len(grouped)
    if rate <= STARTING_RATE_MIN:
        return
    linter(location=protoerror.OVERVIEW)


SOLUTION_2020 = """\
Fußnote Ziffer verwenden

Mindestens {{count}} Fußnote verwenden keine einfache Ziffer 1, 2, 3. \
Überdenken Sie den Stil ihrer Fußnoten.

{text/fussnote.html#nummerierung}
"""


def check_2020_special_number(linter, driver):
    numeric, special = utilo.partition(  # pylint:disable=unused-variable
        key=lambda x: x[1].raw_number is None or x[1].raw_number.isnumeric(),
        items=driver.footnotes,
    )
    if len(special) <= FOOTNOTE_SPECIAL_NUMBER_MAX:
        return
    rate = len(special) / len(driver.footnotes)
    if rate < FOOTNOTE_SPECIAL_RATE_MAX:
        return
    linter(
        count=len(special),
        location=protoerror.OVERVIEW,
    )


FOOTNOTE_SPECIAL_NUMBER_MAX = configos.HV_INT_PLUS(default=15)

FOOTNOTE_SPECIAL_RATE_MAX = configos.HV_PERCENT_PLUS(default=30)


def starting(items: list) -> bool:
    """Footnotes starts with `1, 2, 3, 4, 5`.

    >>> starting((1, 2, 3, 4, 5, 6, 7, 8, 10, 11))
    True
    >>> starting((3, 4, 5))
    False
    """
    # TODO: USE utilo.isascending?
    result = [
        current == expected for current, expected in zip(items, range(1, 5))
    ]
    return all(result)

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

import configo
import protocol
import serializeraw
import utila


def work(footerheader: str, pages: tuple = None) -> protocol.ResultType:
    driver = create_driver(
        footerheader=footerheader,
        pages=pages,
    )
    result = protocol.run(
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
    result = protocol.driver(footnotes=footnotes)
    return result


SOLUTION_2015 = """\
Endnoten verwendet

Im Dokument werden Endnoten verwendet. Ersetzen Sie diese durch \
stringend aufsteigende Fußnoten.

TODO: ARTICLE ENDNOTE_VS_FOOTNOTE
"""
# TODO: move MIN_CHECK to a decorator?
# require more than `15` footnote to run this linter
ENDNOTE_CHECK_NUMBER_MIN = configo.HV_INT_PLUS(default=15)

# Decide between endnotes and failing footnotes
STARTING_MIN = configo.HV_INT_PLUS(default=3)

STARTING_RATE_MIN = configo.HV_PERCENT_PLUS(default=80)


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
    if utila.isascending(numbers):
        return
    grouped = utila.groupby_ascending(numbers)
    # TODO : USE CHAINSAW DETECTOR HERE
    started = [item for item in grouped if starting(item)]
    rate = len(started) / len(grouped)
    if rate <= STARTING_RATE_MIN:
        return
    linter(location=protocol.OVERVIEW)


SOLUTION_2020 = """\
Fußnote Ziffer verwenden

Mindestens {{count}} Fußnote verwenden keine einfache Ziffer 1, 2, 3. \
Überdenken Sie den Stil ihrer Fußnoten.

{text/fussnote.html#nummerierung}
"""


def check_2020_special_number(linter, driver):
    numeric, special = utila.partition(  # pylint:disable=unused-variable
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
        location=protocol.OVERVIEW,
    )


FOOTNOTE_SPECIAL_NUMBER_MAX = configo.HV_INT_PLUS(default=15)

FOOTNOTE_SPECIAL_RATE_MAX = configo.HV_PERCENT_PLUS(default=30)


def starting(items: list) -> bool:
    """Footnotes starts with `1, 2, 3, 4, 5`.

    >>> starting((1, 2, 3, 4, 5, 6, 7, 8, 10, 11))
    True
    >>> starting((3, 4, 5))
    False
    """
    # TODO: USE utila.isascending?
    result = [
        current == expected for current, expected in zip(items, range(1, 5))
    ]
    return all(result)

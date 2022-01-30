# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
""".. _decider_features_footnote:

Footnotes
=========
"""

import functools
import typing

import configo
import protocol
import serializeraw
import utila


def work(footerheader: str, pages: tuple = None) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)

    headerfooters = serializeraw.load_footnotes(footerheader, pages)

    linting(headerfooters, linter)

    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(footer, linter: protocol.Linter):
    checkers = protocol.parse_checkers(__name__)

    flat = []
    for page in footer:
        for item in page.content:
            flat.append((page.page, item))

    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
        )
        checker(call, flat)


SOLUTION_2015 = """\
Endnoten verwendet

Im Dokument werden Endnoten verwendet. Ersetzen Sie diese durch \
stringend aufsteigende Fußnoten.

TODO: ARTICEL ENDNOTE_VS_FOOTNOTE
"""
# TODO: move MIN_CHECK to a decorator?
# require more than `15` footnote to run this linter
ENDNOTE_CHECK_NUMBER_MIN = configo.HV_INT_PLUS(default=15)

# Decide between endnotes and failing footnotes
STARTING_MIN = configo.HV_INT_PLUS(default=3)

STARTING_RATE_MIN = configo.HV_PERCENT_PLUS(default=80)


def check_2015_endnotes_using(linter, footnotes):
    numbers = [
        item.number for _, item in footnotes if isinstance(item.number, int)
    ]
    if len(numbers) < ENDNOTE_CHECK_NUMBER_MIN:
        return
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


def check_2020_special_number(linter, footnotes):
    numeric, special = utila.partition(  # pylint:disable=unused-variable
        key=lambda x: x[1].raw_number is None or x[1].raw_number.isnumeric(),
        items=footnotes,
    )
    if len(special) <= FOOTNOTE_SPECIAL_NUMBER_MAX:
        return
    rate = len(special) / len(footnotes)
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

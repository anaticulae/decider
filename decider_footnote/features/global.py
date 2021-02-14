# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

import protocol
import serializeraw
import utila

import decider.features


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
MIN_ENDNOTE_CHECK_NUMBER = 15

# Decide between endnotes and failing footnotes
MIN_STARTING = 3
MIN_STARTING_RATE = 0.8


def check_2015_endnotes_using(linter, footnotes):
    numbers = [
        item.number for _, item in footnotes if isinstance(item.number, int)
    ]
    if len(numbers) < MIN_ENDNOTE_CHECK_NUMBER:
        return
    if utila.isascending(numbers):
        return

    grouped = group_raising(numbers)

    # TODO : USE CHAINSAW DETECTOR HERE
    started = [item for item in grouped if starting(item)]
    rate = len(started) / len(grouped)

    if rate <= MIN_STARTING_RATE:
        return

    linter(location=decider.features.OVERVIEW)


def group_raising(items: utila.Numbers):
    if not items:
        return []
    result = [[items[0]]]
    for item in items[1:]:
        if item <= result[-1][-1]:
            # new group
            result.append([item])
        else:
            result[-1].append(item)
    return result


def starting(items):
    """Footnotes starts with `1, 2, 3, 4, 5`."""
    result = [
        current == expected for current, expected in zip(items, range(1, 5))
    ]
    return all(result)

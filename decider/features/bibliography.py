# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import functools
import typing

import detector.bibliography.data
import iamraw
import protocol
import serializeraw
import texmex
import texmex.alpha
import utila


def alphabetically(item: str) -> str:
    if item is None:
        # sort at the end, use max value
        return chr(0x10ffff)
    return texmex.alpha.replace(item).lower()


texmex.alphabetically = alphabetically


def work(table: str) -> typing.Tuple[str, str]:
    loaded = serializeraw.load_bibliography_reference(table)
    with contextlib.suppress(AttributeError):
        # TODO: REMOVE LATER
        if isinstance(loaded[0], list):
            loaded = utila.flatten(loaded)
    linter = protocol.from_module(__name__)
    linting(loaded, linter)
    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(
        references: iamraw.BibliographyReferences,
        linter: protocol.Linter,
):
    location = protocol.Location.from_page(0)
    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
            location=location,
        )
        checker(call, references)


SOLUTION_6000 = """\
Quellenverzeichnis ist nicht alphabetisch sortiert

Sortieren Sie das Quellenverzeichnis.

Gefunden:
---------
{%current%}

Erwartet:
---------
{%expected%}

{elemente/literaturverzeichnis}
"""


def check_6000_not_sorted_alphabetically(
        linter: callable,
        references: iamraw.BibliographyReferences,
):
    current = [item for item in references]
    expected = detector.bibliography.data.theissen_sort(current)
    if current == expected:
        return

    current = [f' * {item.reference}' for item in expected]
    linter(
        current=utila.NEWLINE.join(current),
        expected=utila.NEWLINE.join(expected),
    )

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

import detector.bibliography.order
import iamraw
import protocol
import serializeraw
import utila


def work(table: str) -> typing.Tuple[str, str]:
    loaded = load_bibliography_reference(table)
    linter = protocol.from_module(__name__)
    linting(loaded, linter)
    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def load_bibliography_reference(path) -> list:
    loaded = serializeraw.load_bibliography_reference(path)
    if not loaded:
        return []
    with contextlib.suppress(AttributeError):
        # TODO: REMOVE LATER
        if isinstance(loaded[0], list):
            loaded = utila.flatten(loaded)
    return loaded


def linting(
        references: iamraw.BibliographyReferences,
        linter: protocol.Linter,
):
    location = iamraw.Location.from_page(0)
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
{{current}}

Erwartet:
---------
{{expected}}

{elemente/literaturverzeichnis}
"""


def format_bibline(item) -> str:
    if item.reference:
        return item.reference
    return f' * {item.author} {item.year} {item.title}'


def check_6000_not_sorted_alphabetically(
        linter: callable,
        references: iamraw.BibliographyReferences,
):
    current = [item for item in references]
    expected = detector.bibliography.order.theissen_sort(current)

    if current == expected:
        return

    # TODO: CHECK REPRESENTATION
    current = [format_bibline(item) for item in current]
    expected = [format_bibline(item) for item in expected]

    linter(
        current=utila.NEWLINE.join(current),
        expected=utila.NEWLINE.join(expected),
    )

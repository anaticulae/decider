# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import typing

import groupme.abbreviation
import groupme.abbreviation.dumper as gad
import protocol
import utila

import decider.utils.abbreviation


def work(abbreviations: str) -> typing.Tuple[str, str]:
    abbreviations = gad.load_abbreviation_table(abbreviations)
    linter = protocol.from_module(__name__)
    linting(abbreviations, linter)
    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(
        abbreviations: groupme.abbreviation.AbbreviationResult,
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
        checker(call, abbreviations)


SOLUTION_5000 = """\
Abkuerzungsverzeichnis is nicht alphabetisch sortiert

Sortieren Sie das Abkuerzungsverzeichis.

Gefunden:
---------
{%current%}

Erwartet:
---------
{%expected%}
"""


def check_5000_not_sorted_alphabetically(
        linter: callable,
        table: groupme.abbreviation.AbbreviationResult,
):
    current = [item for item in table]

    if sorted(current) == current:
        return

    expected = [f' * {item.short}' for item in sorted(current)]
    current = [f' * {item.short}' for item in current]
    linter(
        current=utila.NEWLINE.join(current),
        expected=utila.NEWLINE.join(expected),
    )


SOLUTION_5001 = """\
Abkuerzung allgemein bekannt

Die Abkuerzung {%short%}({%description%}) muss nicht separat geklaert
werden, da diese Algemeingueltigkeit besitzt.

Tipp: Entfernen, um das Verzeichnis nicht aufzublaehen.
"""


def check_5001_german_default(
        linter: callable,
        table: groupme.abbreviation.AbbreviationResult,
):
    for item in table:
        try:
            description = decider.utils.abbreviation.DUDEN[item.short]
        except KeyError:
            continue
        linter(short=item.short, description=description)

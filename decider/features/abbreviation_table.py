# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import typing

import iamraw
import konrad
import protocol
import serializeraw
import utila


def work(abbreviations: str) -> typing.Tuple[str, str]:
    abbreviations = serializeraw.load_abbreviation_table(abbreviations)
    linter = protocol.from_module(__name__)
    linting(abbreviations, linter)
    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(
        abbreviations: iamraw.AbbreviationResult,
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
        checker(call, abbreviations)


SOLUTION_5000 = """\
Abkürzungsverzeichnis ist nicht alphabetisch sortiert

Sortieren Sie das Abkürzungsverzeichnis.

Gefunden:
---------
{{current}}

Erwartet:
---------
{{expected}}

{elemente/abkuerzungsverzeichnis#alphabetische-sortierung}
"""


def check_5000_not_sorted_alphabetically(
        linter: callable,
        table: iamraw.AbbreviationResult,
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


SOLUTION_R5001 = """\
Abkürzung allgemein bekannt

Die Abkürzung {{short}}({{description}}) muss nicht separat erklärt
werden, da diese Allgemeingültingkeit besitzt.

Tipp: Abkürzung entfernen zur Erhöhung der Übersichtlichkeit

{elemente/abkuerzungsverzeichnis#abkurzungsverzeichnis}
"""


def check_5001_german_default(
        linter: callable,
        table: iamraw.AbbreviationResult,
):
    for item in table:
        try:
            # TODO: INTRODUCE METOD TO CHECK LOWER-, UPPERCASE and spelling errors
            description = konrad.ABBREVIATION[item.short]
        except KeyError:
            continue
        linter(short=item.short, description=description)

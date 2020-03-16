# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abbreviation Text Behavior
==========================

This module verifies the described abbreviation in textual flow.

TODO:

* No abbreviation at sentence start
* Insert `Festabstand` between characters
* No Linebreak inside abbreviation
* Ensure no artikel before abbreviation: " S.5. Bd. 6" but "die Seite 5,
  der Band 8"

[Source DUDEN]
"""

import functools
import itertools
import typing

import groupme.abbreviation
import groupme.abbreviation.dumper as gad
import protocol
import words.abbreviation.loader


def work(abbreviations: str, text: str) -> typing.Tuple[str, str]:
    abbreviations = gad.load_abbreviation_table(abbreviations)
    text = words.abbreviation.loader.load_text_abbreviations(text)

    linter = protocol.from_module(__name__)
    linting(abbreviations, text, linter)
    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(
        abbreviations: groupme.abbreviation.AbbreviationResult,
        text: words.abbreviation.loader.ExtractedTextAbbreviations,
        linter: protocol.Linter,
):
    location = protocol.Location.from_page(0)
    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        print(checker)
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
            location=location,
        )
        checker(call, abbreviations, text)


SOLUTION_5100 = """\
Abkuerzung wurde vor der Definition benutzt

Die Abkuerzung "{%short%}" wurde auf Seite {%before_page%}, Satz {%before_sentence%}
benutzt bevor sie auf Seite {%definition_page%}, Satz {%definition_sentence%}
definiert wurde.

Definieren Sie die Abkuerzung an der ersten Stelle des Gebrauchs.

{text/abkuerzung#abkurzung}
"""


def check_5100_used_before_defined(
        linter: callable,
        table: groupme.abbreviation.AbbreviationResult,  # pylint:disable=W0613
        text: words.abbreviation.loader.ExtractedTextAbbreviations,
):
    # TODO: Use table to verify lintings?
    flat = flat_abbreviation(text)
    grouped = itertools.groupby(flat, key=lambda x: x.short)
    for key, values in grouped:
        values = list(values)
        if len(values) == 1:
            continue
        if values[0].description is not None:
            # abbreviation is defined at first occurrence
            continue
        defined_later = [
            item for item in values[1:] if item.description is not None
        ]
        if not any(defined_later):
            # abbreviation is nowhere defined
            continue
        for item in defined_later:
            linter(
                short=key,
                before_page=values[0].position.page,
                before_sentence=values[0].position.sentence,
                definition_page=item.position.page,
                definition_sentence=item.position.page,
            )


def flat_abbreviation(items):
    result = []
    for item in items:
        result.extend(item.content)
    return result


SOLUTION_5110 = """\
Abkuerzung wurde nicht im Text verwerdet

Die Abkuerzung "{%short%}" konnte nicht im Text gefunden werden.
"""


def check_5110_unused_abbreviation(
        linter: callable,
        table: groupme.abbreviation.AbbreviationResult,
        text: words.abbreviation.loader.ExtractedTextAbbreviations,
):
    flat = flat_abbreviation(text)
    unique = {item.short for item in flat}
    for item in table:
        if item.short in unique:
            continue
        linter(short=item.short)

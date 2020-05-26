# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
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

import decider_footnote.footnote


def work(footerheader: str, pages: tuple = None) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)

    headerfooters = decider_footnote.footnote.load(footerheader, pages)

    for footer in headerfooters:
        # run linter
        linting(footer, linter)

    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(footer, linter: protocol.Linter):
    location = protocol.Location.from_page(footer.page)

    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
            location=location,
        )
        for item in footer.content:
            checker(call, item)


SOLUTION_2001 = """\
Fußnote {%number%} beginnt nicht mit einem Großbuchstaben

Ersetzen Sie den ersten Buchstaben der Fußnote {%number%} mit einem
Großbuchstaben.

{text/fussnote#struktur}
"""


def check_2001_no_uppercase_at_start(linter, item):
    """Ensure that footnote starts with uppercase letter."""
    text = item.text.strip()

    if text[0].isupper():
        return

    linter(number=item.number)


SOLUTION_2002 = """\
Die Fußnote {%number%} endet nicht mit einem Punkt

Fügen Sie einen Punkt am Ende der Fußnote {%number%} hinzu.

{text/abkuerzung#abkurzung}
"""


def check_2002_no_dot_at_end(linter, item):
    """Ensure that footnote is closed with an dot '.'."""
    text = item.text.strip()

    if text[-1] == '.':
        return

    linter(number=item.number)

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
import math
import typing

import configo
import protocol
import utila

import decider.footnote

MAX_HIGHNOTE_RISE_DIFF = configo.HV_FLOAT_PLUS(default=0.5).value
MAX_HIGHNOTE_SIZE_DIFF = configo.HV_FLOAT_PLUS(default=0.5).value

MAX_CONTENT_SIZE_DIFF = configo.HV_FLOAT_PLUS(default=0.5).value


def work(footerheader: str, pages: tuple = None) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)

    headerfooters = decider.footnote.load(footerheader, pages)
    footnotes = utila.flatten([item.content for item in headerfooters if item])
    fontconfig = decider.footnote.most_common_font(footnotes)

    for footer in headerfooters:
        # run linter
        linting(footer.content, fontconfig, footer.page, linter)

    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


# TODO: ADD GENERAL PACKAGE TO DEFINE UNIQUE IDS
FOOTER_CHECKER_ID = 20


def linting(
        items,
        fontconfig: decider.footnote.FootNoteStyle,
        page: int,
        linter: protocol.Linter,
):
    location = protocol.Location.from_page(page)

    if fontconfig:
        # validation requires valid font config
        datum = protocol.driver(
            location=location,
            fontconfig=fontconfig,
        )
    else:
        datum = protocol.driver(location=location)

    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
            location=location,
        )
        for item in items:
            try:
                checker(call, item, datum)
            except TypeError:
                # no `datum` required
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


SOLUTION_2003 = """\
Fußnote {%number%} invalid highnote rise

Expected: {%expected%} != Current: {%current%}

{text/fussnote#formatierung}
"""


def check_2003_invalid_highnote_rise(linter, item, data):
    """Ensure that footnote fits to `common` footnote highnote numer rise."""
    current = item.style[0].rise
    expected = data.fontconfig.highnote_rise

    if equal(current, expected, MAX_HIGHNOTE_RISE_DIFF):
        return

    linter(
        number=item.number,
        current=current,
        expected=expected,
    )


SOLUTION_2004 = """\
Fußnote {%number%}: invalid highnote size

Expected: {%expected%} != Current: {%current%}

{text/fussnote#formatierung}
"""


def check_2004_invalid_hignote_size(linter, item, data):
    """Ensure correct font size of highnote."""
    current = item.style[0].size
    expected = data.fontconfig.highnote_size

    if equal(current, expected, MAX_HIGHNOTE_SIZE_DIFF):
        return

    linter(
        number=item.number,
        current=current,
        expected=expected,
    )


SOLUTION_2005 = """\
Fußnote {%number%}: invalid font family

Expected: {%expected%} != Current: {%current%}

{text/fussnote#formatierung}
"""


def check_2005_invalid_highnote_fontfamily(linter, item, data):
    """Ensure correct font family of highnote."""
    current = item.style[0].font
    expected = data.fontconfig.highnote_fontid

    if current == expected:
        return

    linter(
        number=item.number,
        current=current,
        expected=expected,
    )


SOLUTION_2010 = """\
Fußnote {%number%}: invalid content size

Expected: {%expected%} != Current: {%current%}

{text/fussnote#formatierung}
"""


def check_2010_invalid_content_fontsize(linter, item, data):
    """Ensure correct font size of footnote content."""
    expected = data.fontconfig.content_size
    sizes = [item.size for item in item.style[1].content]
    sizes_equal = [
        equal(item, expected, MAX_CONTENT_SIZE_DIFF) for item in sizes
    ]

    if all(sizes_equal):
        return

    linter(
        number=item.number,
        current=sizes,
        expected=expected,
    )


def equal(current, expected, max_diff: float = 0.0001):
    diff = math.fabs(expected - current)
    return diff <= max_diff

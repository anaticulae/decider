# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re
import typing

import iamraw
import protocol
import texmex

import decider_textflow.features


def work(  # pylint:disable=R0914
        headlines: str,
        text: str,
        textpositions: str,
        sizeandborders: str,
        headerfooter: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    driver = decider_textflow.features.textdata(
        headlines,
        text,
        textpositions,
        sizeandborders,
        headerfooter,
        pages=pages,
    )
    result = decider_textflow.features.linting(__name__, driver)
    return result


def check_character(linter, driver, regex):
    text = driver.text_chunks
    for page, line, item in text:
        if isinstance(item, iamraw.Headline):
            continue

        text = item.text
        # TODO: SUPPORT MULTIPLE ERRORS IN ONE LINE
        matched = re.search(regex, text, flags=re.VERBOSE)
        if not matched:
            continue

        # TODO: ADD TOKEN LOCATION
        location = protocol.RangedLocation(page=page, line=line)
        linter(location=location)


SOLUTION_7650 = """\
Unzuläßiges Leerzeichen vor Komma

Ungültiges Leerzeichen vor einem Komma erkannt.
"""

SPACE_BEFORE_COMMA = r'\s+\,'


def check_7650_space_before_comma(linter: callable, driver):
    """\
    >>> message('space before , comma', 7650)
    1
    """
    check_character(linter, driver, SPACE_BEFORE_COMMA)


SOLUTION_7651 = """\
Fehlendes Leerzeichen nach Komma

Fehlendes Leerzeichen nach einem Komma erkannt.
"""

# TODO: ADD RISE to DISTINGUISH OF NORMAL NUMBERS
MISSING_SPACE_AFTER_COMMA = r'\,[a-zA-Z]'


def check_7651_missing_space_after_comma(linter: callable, driver):
    """\
    >>> message('hightnote: ,10', 7651)
    0
    >>> message('normal text: this is helmut,space missing', 7651)
    1
    """
    check_character(linter, driver, MISSING_SPACE_AFTER_COMMA)


SOLUTION_7652 = """\
Unzuläßiges Leerzeichen vor eckiger Klammer

Ungültiges Leerzeichen vor einer eckigen Klammer erkannt.
"""

SPACE_BEFORE_SQUARE_BRACKET = r'[^\[]\s+\]'


def check_7652_space_before_square_bracket(linter: callable, driver):
    """\
    >>> message('[Jens ] space inside author reference', 7652)
    1
    >>> message('[ ] replace with [...]', 7652)
    0
    """
    check_character(linter, driver, SPACE_BEFORE_SQUARE_BRACKET)


SOLUTION_7653 = """\
Unzuläßiges Leerzeichen nach eckiger Klammer

Ungültiges Leerzeichen nach einer eckigen Klammer erkannt.
"""

SPACE_AFTER_SQUARE_BRACKET = r'\[\s+[^\]]'


def check_7653_space_after_square_bracket(linter: callable, driver):
    """\
    >>> message('[ Jens] space inside author reference', 7653)
    1
    >>> message('[ ] replace with [...]', 7653)
    0
    """
    check_character(linter, driver, SPACE_AFTER_SQUARE_BRACKET)


SOLUTION_7654 = """\
Leerzeichen vor Semicolon

Unzuläßiges Leerzeichen vor Semicolon erkannt.

SIEHE SATZZEICHEN
"""

SPACE_BEFORE_SEMICOLON = r'\s+\;'


def check_7654_space_before_semicolon(linter: callable, driver):
    check_character(linter, driver, SPACE_BEFORE_SEMICOLON)


SOLUTION_7655 = """\
Fehlendes Leerzeichen nach Semicolon

Fehlendes Leerzeichen nach Semicolon erkannt.

SIEHE SATZZEICHEN
"""

MISSING_SPACE_AFTER_SEMICOLON = r'\;[^\s]'


def check_7655_missing_space_after_semicolon(linter: callable, driver):
    check_character(linter, driver, MISSING_SPACE_AFTER_SEMICOLON)


SOLUTION_7656 = """\
Fehlerhaftes Auslassungszeichen

Gefunden **[ ]** ersetzen Sie es durch **[...]**
"""

MISSING_DOTS_BETWEEN_ANGLE_BRACKETS = r'\[\s*\]'


def check_7656_missing_dots_between_brackets(linter: callable, driver):
    """\
    >>> message('[] replace with [...]', 7656)
    1
    >>> message('[  ] replace with [...]', 7656)
    1
    """
    check_character(linter, driver, MISSING_DOTS_BETWEEN_ANGLE_BRACKETS)


def message(lines: list, msgid=None, page=0):
    if isinstance(lines, str):
        lines = [lines]
    # page, line, text
    lines = [(
        page,
        line,
        texmex.TextBoundsInfo(text=content, bounds=None),
    ) for line, content in enumerate(lines)]
    driver = protocol.driver(text_chunks=lines)
    user, _ = decider_textflow.features.linting(__name__, driver)
    result = protocol.load_result(user, msgid)
    return len(result)

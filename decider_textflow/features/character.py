# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re
import typing

import iamraw
import protocol
import serializeraw
import texmex

import decider_textflow.features


def work(
        headlines: str,
        text: str,
        textpositions: str,
        sizeandborders: str,
        headerfooter: str,
        magiccontent: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    driver = decider_textflow.features.textdata(
        headlines,
        text,
        textpositions,
        sizeandborders,
        headerfooter,
        magiccontent=magiccontent,
        pages=pages,
    )
    result = decider_textflow.features.linting(__name__, driver)
    return result


def check_character(linter, driver, regex):
    text = driver.nomagic_text_chunks
    for page, line, item in text:
        if isinstance(item, iamraw.Headline):
            continue
        if not item:
            # magic content
            continue

        text = item.text
        # TODO: SUPPORT MULTIPLE ERRORS IN ONE LINE
        matched = re.finditer(regex, text, flags=re.VERBOSE | re.I)
        if not matched:
            continue

        for match in matched:
            start, end = match.span()[0], match.span()[1]
            location = iamraw.RangedLocation(
                page=page,
                line=line,
                char=start,
                char_end=end,
            )
            linter(location=location)


SOLUTION_7650 = """\
Unzuläßiges Leerzeichen vor Komma

Ungültiges Leerzeichen vor einem Komma erkannt.

{darstellung/satzzeichen#komma}
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

{darstellung/satzzeichen#komma}
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

SPACE_BEFORE_SQUARE_BRACKET = r"""
    [^\[\s]     # no open square bracket or space
    \s+         # white space(s) before closing bracket
    \]          # close with square bracket
"""


def check_7652_space_before_square_bracket(linter: callable, driver):
    """\
    >>> message('[Jens ] space inside author reference', 7652)
    1
    >>> message('[] [ ] [  ] [   ] replace with [...]', 7652)
    0
    """
    check_character(linter, driver, SPACE_BEFORE_SQUARE_BRACKET)


SOLUTION_7653 = """\
Unzuläßiges Leerzeichen nach eckiger Klammer

Ungültiges Leerzeichen nach einer eckigen Klammer erkannt.
"""

SPACE_AFTER_SQUARE_BRACKET = r"""
    \[          # start with open square bracket
    \s+?        # one or more space after open square bracket
    (?!\s*\])   # do not end with spaces and ] to distinguish from
                # [ ] error message
"""


def check_7653_space_after_square_bracket(linter: callable, driver):
    """\
    >>> message('[ Jens] space inside author reference', 7653)
    1
    >>> message('[  DoubleSpace]', 7653)
    1
    >>> message('[   ] [  ] [ ] replace with [...]', 7653)
    0
    """
    check_character(linter, driver, SPACE_AFTER_SQUARE_BRACKET)


SOLUTION_7654 = """\
Leerzeichen vor Semikolon

Unzuläßiges Leerzeichen vor Semikolon erkannt.

{darstellung/satzzeichen#semikolon}
"""

SPACE_BEFORE_SEMICOLON = r'\s+\;'


def check_7654_space_before_semicolon(linter: callable, driver):
    check_character(linter, driver, SPACE_BEFORE_SEMICOLON)


SOLUTION_7655 = """\
Fehlendes Leerzeichen nach Semicolon

Fehlendes Leerzeichen nach Semicolon erkannt.

{darstellung/satzzeichen#semikolon}
"""

MISSING_SPACE_AFTER_SEMICOLON = r'\;[^\s]'


def check_7655_missing_space_after_semicolon(linter: callable, driver):
    check_character(linter, driver, MISSING_SPACE_AFTER_SEMICOLON)


SOLUTION_7656 = """\
Fehlerhaftes Auslassungszeichen

Gefunden **[ ]** ersetzen Sie es durch **[...]**

{darstellung/satzzeichen#auslassungspunkte}
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


SOLUTION_7660 = """\
Bindestrich zwischen Ziffer und 'mal' fehlt.

Siehe Duden:

* 2-mal
* fünfhundert Mal
* ein Dutzend Mal

Hinweis: Ziffern werden bei exakten Werten verwendet - ausgeschrieben \
wird die Zahl wenn sie eine ungefähre Zahl beinhaltet.

Siehe GUGELHUPF

TODO ADD LINK
"""

MISSING_MINUS_BETWEEN_VALUE_AND_SIGN = r'\d+(mal)'


def check_7660_missing_minus_value_and_sign(linter: callable, driver):
    """Number in combination with `mal` is connected with minus. But
    `zweihundert Mal` is correct, no minus is needed.

    >>> message('300mal ist nicht so gut wie 600-mal', 7660)
    1
    """
    check_character(linter, driver, MISSING_MINUS_BETWEEN_VALUE_AND_SIGN)


SOLUTION_7661 = """\
Schrägstrich: Überflüssiges Leerzeichen

Vor und nach einem Schrägstrich wird kein Leerzeichen gesetzt.

{darstellung/satzzeichen#divis}
"""

SPACE_BEFORE_OR_AFTER_SLASH = r'(\s+/\s+|\s+/|/\s+)'


def check_7661_space_before_or_after_slash(linter: callable, driver):
    """\
    >>> message('Europäischen Gemeinschaften (Beutler / Bieber / Pipkorn / Streil 2001).', 7661)
    3
    >>> message('Bitte wählen Mann/ Frau., 7661')
    1
    >>> message('dieser bei 1.44/1.63, den Mittelaltrigen bei 0.72/0.483', 7661)
    0
    """
    check_character(linter, driver, SPACE_BEFORE_OR_AFTER_SLASH)


SOLUTION_7662 = """\
Fehlendes Leerzeichen nach Paragraf

Zwischen Paragrafzeichen und der Paragrafnummer wird ein Festabstand gesetzt.

{darstellung/satzzeichen#paragrafzeichen}
"""

SPACE_AFTER_PARAGRAPH = r'§\d+[a-z]?'


def check_7662_space_after_paragraph(linter: callable, driver):
    """\
    >>> message('StVG §24c „ […] wer in der Probezeit nach §2a oder vor', 7662)
    2
    >>> message('um eine Straftat nach § 316, welches', 7662)
    0
    """
    check_character(linter, driver, SPACE_AFTER_PARAGRAPH)


SOLUTION_7663 = """\
Bindestrich fehlt

Siehe Duden:

* vierjährig
* 4-jährig
* Fünfjähriger
* die 4- bis 5-Jährigen

TODO ADD LINK
"""

MISSING_MINUS_BETWEEN = r'\d+(jährig)(en){0,1}'


def check_7663_missing_minus_number_jaehrig(linter: callable, driver):
    """\
    >>> message('25jährigen und die ab 69jährigen in Unfälle verwickelt waren.', 7663)
    2
    """
    check_character(linter, driver, MISSING_MINUS_BETWEEN)


SOLUTION_7665 = """\
Unnötige Genauigkeit

Zahlen geschrieben als Ziffern symbolisieren eine exakte Genauigkeit. \
Diese Genauigkeit wird durch den Zusatz **circa, ca. oder etwa** \
relativiert. Schreiben Sie die Zahl aus um dies deutlich zu machen.

{darstellung/schreibweise#zahlen}
"""

WRONG_ACCURACY = r'(etwa|circa|\bca\.?\b)[ ]{0,4}\d+'


def check_7665_wrong_accuracy(linter: callable, driver):
    """\
    >>> message('Etwa 1000 Einwohner wohnen hier. Circa 12 Menschen wohnen hier.', 7665)
    2
    """
    check_character(linter, driver, WRONG_ACCURACY)


def message(lines: list, msgid=None, page=0):
    if isinstance(lines, str):
        lines = [lines]
    # page, line, text
    lines = [(
        page,
        line,
        texmex.TextBoundsInfo(text=content, bounds=None),
    ) for line, content in enumerate(lines)]
    driver = protocol.driver(text_chunks=lines, nomagic_text_chunks=lines)
    user, _ = decider_textflow.features.linting(__name__, driver)
    result = serializeraw.load_findings(user, msgid)
    return len(result)

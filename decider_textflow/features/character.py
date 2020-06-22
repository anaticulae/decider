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


SOLUTION_7650 = """\
Unzuläßiges Leerzeichen vor Komma

Ungültiges Leerzeichen vor einem Komma erkannt.
"""

SPACE_BEFORE_COMMA = r'\s+\,'


def check_7650_space_before_comma(linter: callable, driver):
    text = driver.text_chunks
    for page, line, item in text:
        if isinstance(item, iamraw.Headline):
            continue

        text = item.text
        # TODO: SUPPORT MULTIPLE ERRORS IN ONE LINE
        matched = re.search(SPACE_BEFORE_COMMA, text)
        if not matched:
            continue

        # TODO: ADD TOKEN LOCATION
        location = protocol.RangedLocation(page=page, line=line)
        linter(location=location)


SOLUTION_7651 = """\
Fehlendes Leerzeichen nach Komma

Fehlendes Leerzeichen nach einem Komma erkannt.
"""

MISSING_SPACE_AFTER_COMMA = r'\,\w'


def check_7651_missing_space_after_comma(linter: callable, driver):
    text = driver.text_chunks
    for page, line, item in text:
        if isinstance(item, iamraw.Headline):
            continue

        text = item.text
        # TODO: SUPPORT MULTIPLE ERRORS IN ONE LINE
        matched = re.search(MISSING_SPACE_AFTER_COMMA, text)
        if not matched:
            continue

        # TODO: ADD TOKEN LOCATION
        location = protocol.RangedLocation(page=page, line=line)
        linter(location=location)


SOLUTION_7652 = """\
Unzuläßiges Leerzeichen vor eckiger Klammer

Ungültiges Leerzeichen vor einer eckigen Klammer erkannt.
"""

SPACE_BEFORE_SQUARE_BRACKET = r'\s+\]'


def check_7652_space_before_square_bracket(linter: callable, driver):
    text = driver.text_chunks
    for page, line, item in text:
        if isinstance(item, iamraw.Headline):
            continue

        text = item.text
        # TODO: SUPPORT MULTIPLE ERRORS IN ONE LINE
        matched = re.search(SPACE_BEFORE_SQUARE_BRACKET, text)
        if not matched:
            continue

        # TODO: ADD TOKEN LOCATION
        location = protocol.RangedLocation(page=page, line=line)
        linter(location=location)


SOLUTION_7653 = """\
Unzuläßiges Leerzeichen nach eckiger Klammer

Ungültiges Leerzeichen nach einer eckigen Klammer erkannt.
"""

SPACE_AFTER_SQUARE_BRACKET = r'\[\s+'


def check_7653_space_after_square_bracket(linter: callable, driver):
    text = driver.text_chunks
    for page, line, item in text:
        if isinstance(item, iamraw.Headline):
            continue

        text = item.text
        # TODO: SUPPORT MULTIPLE ERRORS IN ONE LINE
        matched = re.search(SPACE_AFTER_SQUARE_BRACKET, text)
        if not matched:
            continue

        # TODO: ADD TOKEN LOCATION
        location = protocol.RangedLocation(page=page, line=line)
        linter(location=location)


SOLUTION_7654 = """\
Fehlendes Leerzeichen vor Semicolon

Fehlendes Leerzeichen vor Semicolon erkannt.
"""

MISSING_SPACE_BEFORE_SEMICOLON = r'\s+\;'


def check_7654_space_before_semicolon(linter: callable, driver):
    text = driver.text_chunks
    for page, line, item in text:
        if isinstance(item, iamraw.Headline):
            continue

        text = item.text
        # TODO: SUPPORT MULTIPLE ERRORS IN ONE LINE
        matched = re.search(MISSING_SPACE_BEFORE_SEMICOLON, text)
        if not matched:
            continue

        # TODO: ADD TOKEN LOCATION
        location = protocol.RangedLocation(page=page, line=line)
        linter(location=location)

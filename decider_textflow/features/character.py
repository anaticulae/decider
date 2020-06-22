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

import german
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

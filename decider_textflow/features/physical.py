# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

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


SOLUTION_7670 = """\
Fehlendes Leerzeichen nach Wert?

Zwischen physikalischer Einheit und Wert? fehlt ein Leerzeichen.
"""


def check_7670_missing_space_after_value(linter: callable, driver):
    text = driver.text_chunks
    for page, line, item in text:
        if isinstance(item, iamraw.Headline):
            continue

        text = item.text
        # TODO: SUPPORT MULTIPLE ERRORS IN ONE LINE
        finding = extract_units(text)  # pylint:disable=E1128
        if not finding:
            continue

        location = protocol.RangedLocation(page=page, line=line)
        linter(location=location)


# TODO:  IMPROVE THIS DRAFT


def extract_units(text: str) -> list:  # pylint:disable=W0613
    return None

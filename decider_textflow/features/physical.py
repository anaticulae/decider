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
Fehlendes Leerzeichen

Zwischen Skalar **{{value}}** und Einheit **{{unit}}** fehlt ein \
Leerzeichen.

TODO: ADD LINK
DUDEN
"""

UNITS = r'%|‰|km/h|mmHg|mm|ms|m|cm|V|W|Hz|mW'
MISSING_SPACE_BEFORE_UNIT = r'(?P<value>\d+((\.|\,)\d+){0,1})(?P<unit>' + UNITS + r')'


def check_7670_missing_space_after_value(linter: callable, driver):
    """\
    >>> message('10.0% Guthaben', 7670)
    1
    >>> message('Fahrer unter Alkoholeinfluss (0.5‰) wurden', 7670)
    1
    >>> message('einer Geschwindigkeit von 100km/h dazu, dass noch 2,8m zurückgelegt werden, bevor', 7670)
    2
    """
    text = driver.text_chunks
    for page, line, item in text:
        if isinstance(item, iamraw.Headline):
            continue
        text = item.text
        matched = re.finditer(MISSING_SPACE_BEFORE_UNIT, text)
        if not matched:
            continue
        for finding in matched:
            unit, value = finding['unit'], finding['value']
            location = iamraw.RangedLocation(page=page, line=line)
            linter(location=location, unit=unit, value=value)


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

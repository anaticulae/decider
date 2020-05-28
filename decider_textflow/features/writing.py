# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

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


SOLUTION_7600 = """\
Fehler in der Persepektive

**{%invalid%}** sollte vermieden werden.

TODO: ADD ARTICLE
"""

# TODO: REPLACE WITH EXTERNAL METHOD
INVALID_PERSPECTIVE = {'wir', 'man', 'Wir', 'Man'}


def check_7600_text_perspective(linter: callable, driver):
    text = driver.text_chunks
    for page, line, item in text:
        if isinstance(item, iamraw.Headline):
            continue

        words = german.split_words(item.text, validate_sentences=False)
        words = [item.lower() for item in words if isinstance(item, str)]
        # TODO: DO NOT LINT IN QUOTATION
        invalid = [item for item in words if item in INVALID_PERSPECTIVE]
        if not invalid:
            continue
        location = protocol.RangedLocation(page=page, line=line)
        linter(location=location, invalid=', '.join(invalid))

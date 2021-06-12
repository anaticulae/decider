# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import german
import iamraw

import decider_textflow.features

TEXTUAL = {
    iamraw.PageContentType.TEXT,
}


def work(
    headlines: str,
    text: str,
    textpositions: str,
    sizeandborders: str,
    headerfooter: str,
    magiccontent: str,
    quotations: str,
    pages: tuple = None,
) -> typing.Tuple[str, str]:
    driver = decider_textflow.features.textdata(
        headlines,
        text,
        textpositions,
        sizeandborders,
        headerfooter,
        magiccontent=magiccontent,
        magicvalid=TEXTUAL,
        quotations=quotations,
        pages=pages,
    )
    result = decider_textflow.features.linting(__name__, driver)
    return result


SOLUTION_7600 = """\
Fehler in der Perspektive

**{{invalid}}** sollte vermieden werden.

{text/stilkunde/perspektive}
"""

# TODO: REPLACE WITH EXTERNAL METHOD
INVALID_PERSPECTIVE = {'wir', 'man', 'Wir', 'Man'}


def check_7600_text_perspective(linter: callable, driver):
    text = driver.text_chunks
    for page, line, item in text:
        if isinstance(item, iamraw.Headline):
            continue
        if not item:
            # list, quotation or something
            continue

        words = german.word_tokenize(item.text, validate_sentences=False)
        words = [item.lower() for item in words if isinstance(item, str)]
        # TODO: DO NOT LINT IN QUOTATION
        invalid = [item for item in words if item in INVALID_PERSPECTIVE]
        if not invalid:
            continue
        location = iamraw.RangedLocation(page=page, line=line)
        linter(location=location, invalid=', '.join(invalid))

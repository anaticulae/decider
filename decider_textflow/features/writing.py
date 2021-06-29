# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import typing

import german
import iamraw
import konrad
import utila

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

**{{invalid}}** im Satz: **{{line}}** sollte vermieden werden.

{text/stilkunde/perspektive}
"""


def check_7600_text_perspective(linter: callable, driver):
    text = driver.text_chunks
    # group quotes by page
    quotes = collections.defaultdict(list)
    for quote in driver.quotations:
        quotes[quote.page].append(quote.sentence)
    # group text content
    grouped = groupby_page(driver.text_chunks)
    for page, textraw in grouped.items():
        text = german.word_tokenize(textraw, validate_sentences=False)
        text = ' '.join(konrad.mark2str(item) for item in text)
        text = remove_quotes(text, quotes[page])
        for sentence in german.sentence_tokenize(text):
            tokens = german.word_tokenize(sentence, validate_sentences=False)
            invalid = invalid_perspective(tokens)
            if not invalid:
                continue
            # convert token sentence to user sentence with correct spaces
            # and punctuation.
            sentence = german.sentence_select(textraw, tokens)
            # TODO: CENTER SENTENCE TO FINDING, REDUCE SENTENCE LENGTH
            sentence = utila.normalize_text(sentence, normalize_spaces=True)
            # TODO: DETERMINE SENTENCE/LINE NUMBER
            line = 0
            location = iamraw.RangedLocation(page=page, line=line)
            linter(
                location=location,
                invalid=', '.join(invalid),
                line=sentence,
            )


def groupby_page(text):
    grouped = collections.defaultdict(list)
    for page, _, item in text:
        if isinstance(item, iamraw.Headline):
            continue
        if not item:
            # list, quotation or something
            continue
        text = item.text.strip()
        grouped[page].append(text)
    joined = {page: ' '.join(content) for page, content in grouped.items()}
    return joined


def remove_quotes(text, quotes):
    if not quotes:
        return text
    for remove in quotes:
        text = text.replace(remove, '')
    text = utila.normalize_text(text)
    return text


INVALID_PERSPECTIVE = {'wir', 'man'}


def invalid_perspective(words) -> list:
    # TODO: REPLACE WITH EXTERNAL METHOD
    words = [word for word in words if isinstance(word, str)]
    words = [word for word in words if word.lower() in INVALID_PERSPECTIVE]
    return words

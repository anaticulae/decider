# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import german
import iamraw
import konrad
import protocol
import utila

import decider_textflow.features
import decider_textflow.writing.complexity
import decider_textflow.writing.perspective

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
    words: str,
    pages: tuple = None,
) -> protocol.ResultType:
    driver = decider_textflow.features.textdata(
        headlines,
        text,
        textpositions,
        sizeandborders,
        headerfooter,
        magiccontent=magiccontent,
        magicvalid=TEXTUAL,
        quotations=quotations,
        words=words,
        pages=pages,
    )
    result = protocol.run(
        modulename=__name__,
        driver=driver,
    )
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
        # TODO: DO WE ALREADY REQUIRE THIS?
        text = german.word_tokenize(textraw, validate_sentences=False)
        text = ' '.join(konrad.mark2str(item) for item in text)
        text = remove_quotes(text, quotes[page])
        for sentence in german.sentence_tokenize(text):
            tokens = german.word_tokenize(sentence, validate_sentences=False)
            invalid = decider_textflow.writing.perspective.invalid_perspective(tokens)  # yapf:disable
            if not invalid:
                continue
            # convert token sentence to user sentence with correct spaces
            # and punctuation.
            # Remove - as a result of word-division
            tokens = [item for item in tokens if item != konrad.Mark.HYPHEN]
            sentence = german.sentence_select(textraw, tokens)
            if not sentence:
                utila.error(f'could not select sentence: {tokens}')
                utila.error(textraw)
                continue
            # TODO: CENTER SENTENCE TO FINDING, REDUCE SENTENCE LENGTH
            sentence = utila.normalize_text(sentence, normalize_spaces=True)
            # TODO: DETERMINE SENTENCE/LINE NUMBER
            # line = 0
            # location = iamraw.RangedLocation(page=page, line=line)
            location = iamraw.RangedLocation(page=page)
            linter(
                location=location,
                invalid=', '.join(invalid),
                line=sentence,
            )


SOLUTION_7605 = """\
Satz zu lang

Satz *{{line}}* überschreitet Limit. Anzahl der Zeichen({{numbers}}) \
zu hoch.
"""

MAX_SENTENCE_LENGTH = 400  # TODO: HOLY VALUE


def check_7605_text_too_long(linter: callable, driver):
    # group text content
    for sentence in driver.sentences:
        try:
            line, page, number = sentence
        except TypeError:
            # headline
            continue
        if ':' in line:
            # TODO: SPLIT LINE AND JUDGE LATER?
            # Vor allem die sozialen Online-Netzwerke erfreuen sich großer
            # Beliebtheit: Circa zwei Drittel aller Internetnutzer.
            continue
        if len(line) < MAX_SENTENCE_LENGTH:
            continue
        # TODO: CONVERT NUMBER TO LINE
        location = iamraw.RangedLocation(page=page, line=number)
        linter(
            line=line,
            numbers=len(line),
            location=location,
        )


SOLUTION_7606 = """\
Satz zu komplex

Die Komplexität des Satzes **{{line}}** sollte reduziert werden.
"""


def check_7606_text_too_complex(linter: callable, driver):
    for sentence in driver.sentences:
        try:
            line, page, number = sentence
        except TypeError:
            # headline
            continue
        if not decider_textflow.writing.complexity.too_complex(line):
            continue
        # TODO: CONVERT NUMBER TO LINE
        location = iamraw.RangedLocation(page=page, line=number)
        linter(
            line=line,
            location=location,
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
        removed = german.sentence_select(text, remove)
        if not removed:
            utila.error(f'could not find text: {remove}')
            continue
        text = text.replace(removed, '', 1)
    text = utila.normalize_text(text)
    return text

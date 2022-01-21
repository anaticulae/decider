# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import dataclasses

import configo
import german
import iamraw
import protocol
import utila

import decider_textflow.features
import decider_textflow.utils
import decider_textflow.writing.complexity
import decider_textflow.writing.perspective
import decider_textflow.writing.statistics

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


@protocol.german
def check_7600_text_perspective(linter: callable, driver):
    # TODO: REMOVE QUOTES
    for sentence in driver.sentences:
        try:
            line, page, number = sentence
        except TypeError:
            # headline
            continue
        # TODO: CHANGE PERSPECTIVE CHECKER FOR LISTS?
        line, _ = decider_textflow.utils.list_split(line)
        tokens = german.word_tokenize(line, validate_sentences=False)
        invalid = decider_textflow.writing.perspective.invalid(tokens)
        if not invalid:
            continue
        location = iamraw.RangedLocation(page=page, line=number)
        linter(
            location=location,
            invalid=', '.join(invalid),
            line=line,
        )
    # # group quotes by page
    # quotes = collections.defaultdict(list)
    # for quote in driver.quotations:
    #     quotes[quote.page].append(quote.sentence)
    # # group text content
    # grouped = groupby_page(driver.text_chunks)
    # for page, textraw in grouped.items():
    #     # TODO: DO WE ALREADY REQUIRE THIS?
    #     text = german.word_tokenize(textraw, validate_sentences=False)
    #     text = ' '.join(konrad.mark2str(item) for item in text)
    #     text = remove_quotes(text, quotes[page])
    #     for sentence in german.sentence_tokenize(text):
    #         tokens = german.word_tokenize(sentence, validate_sentences=False)
    #         invalid = decider_textflow.writing.perspective.invalid(tokens)
    #         if not invalid:
    #             continue
    #         # convert token sentence to user sentence with correct spaces
    #         # and punctuation.
    #         # Remove - as a result of word-division
    #         tokens = [item for item in tokens if item != konrad.Mark.HYPHEN]
    #         sentence = german.sentence_select(textraw, tokens)
    #         if not sentence:
    #             utila.error(f'could not select sentence: {tokens}')
    #             utila.error(textraw)
    #             continue
    #         # TODO: CENTER SENTENCE TO FINDING, REDUCE SENTENCE LENGTH
    #         sentence = utila.normalize_text(sentence, normalize_spaces=True)
    #         # TODO: DETERMINE SENTENCE/LINE NUMBER
    #         # line = 0
    #         # location = iamraw.RangedLocation(page=page, line=line)
    #         location = iamraw.RangedLocation(page=page)
    #         linter(
    #             location=location,
    #             invalid=', '.join(invalid),
    #             line=sentence,
    #         )


SOLUTION_7605 = """\
Satz zu lang

Satz *{{line}}* überschreitet Limit. Anzahl der Zeichen({{numbers}}) \
zu hoch.
"""

SENTENCE_LENGTH_MAX = configo.HV_INT_PLUS(default=400)


def check_7605_text_too_long(linter: callable, driver):
    # group text content
    for sentence in driver.sentences:
        try:
            line, page, number = sentence
        except TypeError:
            # headline
            continue
        # TODO: CHANGE SENTENCE_LENGTH_MAX FOR LISTS?
        line, _ = decider_textflow.utils.list_split(line)
        if ':' in line:
            # TODO: SPLIT LINE AND JUDGE LATER?
            # Vor allem die sozialen Online-Netzwerke erfreuen sich großer
            # Beliebtheit: Circa zwei Drittel aller Internetnutzer.
            continue
        if len(line) < SENTENCE_LENGTH_MAX:
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


SOLUTION_7610 = """\
Satzmuster wiederholt sich

Der Satzteil **{{sentence}}** wird {{occurence}}-mal im Dokument auf den \
Seiten **{{pages}}** verwendet.
"""


def check_7610_sentence_pattern(linter: callable, driver):
    sentences = driver.sentences
    if not sentences:
        return
    sentences = decider_textflow.writing.utils.determine_sentences(sentences)
    repeating = decider_textflow.writing.perspective.repeating_sentence(
        sentences,
        window=SENTENCE_PATTERN_WINDOW,
        occurence_min=SENTENCE_PATTERN_OCCURENCE_MIN,
    )
    for txt, occurence in repeating:
        pages = [item[0] for item in occurence]
        location = iamraw.Location(page=pages[0])
        linter(
            sentence=txt,
            pages=utila.from_tuple(pages, separator=', '),
            location=location,
            occurence=len(occurence),
        )


SENTENCE_PATTERN_WINDOW = configo.HV_INT_PLUS(default=5)

SENTENCE_PATTERN_OCCURENCE_MIN = configo.HV_INT_PLUS(default=3)

SOLUTION_7611 = """\
Satzanfang wiederholt sich

Der Satzanfang **{{sentence_start}}** wiederholt sich in den folgenden \
Sätzen {{repetition}}-mal.
"""


def check_7611_sentence_start(linter: callable, driver):
    sentences = driver.sentences
    if not sentences:
        return
    sentences = decider_textflow.writing.utils.determine_sentences(
        sentences,
        special_skip=True,
    )
    single = utila.Single()
    for window in range(5, 0, -1):
        equals = decider_textflow.writing.perspective.repeating_sentence_start(
            sentences,
            window=window,
        )
        for group in equals:
            if any(single.contains(item[1:3]) for item in group):
                # already done in a higher window
                continue
            first = group[0]
            sentence_start = ' '.join(first[0])
            location = iamraw.RangedLocation(page=first[1], line=first[2])
            linter(
                sentence_start=sentence_start,
                repetition=len(group),
                location=location,
            )


SOLUTION_7616 = """\
Writing statistics

Wörter: {{words}}
Sätze: {{sentences}}

Wortlänge min: {{word_min}}
Wortlänge avg: {{word_avg}}
Wortlänge max: {{word_max}}

Satzlänge min: {{sentence_min}}
Satzlänge avg: {{sentence_avg}}
Satzlänge max: {{sentence_max}}
"""


def check_7616_writing_statistics(linter: callable, driver):
    sentences = driver.sentences
    if not sentences:
        return
    statistic = decider_textflow.writing.statistics.determine(sentences)
    if not statistic:
        return
    linter(
        **dataclasses.asdict(statistic),
        location=protocol.OVERVIEW,
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

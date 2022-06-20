# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import iamraw
import konrad
import utila

import decider_textflow.docref.matches

SOLUTION_7200 = """\
Referenz nicht gefunden

Der Abbildungs-Verweis **{{reference}}** kann nicht gefunden werden.
"""


def check_7200_figure_reference_exists(linter: callable, driver):
    matcher = decider_textflow.docref.matches.create_matcher(
        references=driver.ref_figure,
        iois=driver.caption_image,
    )
    validated = matcher.validate()
    for invalid in validated.invalid:
        page, data = invalid
        location = iamraw.Location.from_sentence(
            page=page,
            sentence=data.sentence,
        )
        linter(
            location=location,
            reference=data.raw,
        )


SOLUTION_7202 = """\
Referenz nicht gefunden

Der Tabellen-Verweis **{{reference}}** kann nicht gefunden werden.
"""


def check_7202_table_reference_exists(linter: callable, driver):
    captions = caption_numbers(driver.caption_table)
    for reference in driver.ref_table:
        selected = determine_reference(reference, driver.sentences)
        if selected is None:
            utila.error(f'invalid reference: {reference}')
        if reference_exists(selected, captions):
            continue
        location = iamraw.RangedLocation(page=reference.page)
        raw = ', '.join(selected)
        linter(location=location, reference=raw)


def determine_reference(reference, text) -> str:
    selected = utila.select_content(text, page=reference.page)
    marked = reference.marked
    sentence_number = 0
    for section in selected:
        for sentence in section.content:
            if sentence_number == reference.sentence:
                words = [
                    konrad.mark2str(word) for word in german.word_tokenize(
                        sentence,
                        validate_sentences=False,
                    )
                ]
                result = [
                    reference_plain(words[start:end]) for start, end in marked
                ]
                return result
            sentence_number += 1
    return None


def reference_plain(words: list) -> str:
    raw = ' '.join(words)
    raw = raw.replace('( ', '(')
    raw = raw.replace(' )', ')')
    return raw


def caption_numbers(items):
    captions = [item.content for item in items]
    captions = {reference_number(item.raw) for item in utila.flatten(captions)}
    return captions


def reference_exists(reference: list, captions: set) -> bool:
    if reference is None:
        utila.error(f'invalid reference: {reference}, {captions}')
        return True
    refnumber = {reference_number(item) for item in reference}
    diff = refnumber - captions
    # all references are linked if `diff` is empty
    return not diff


def reference_number(reference: str) -> int:
    """\
    >>> reference_number('Abbildung 10: Verschiebung des Order')
    10
    >>> reference_number('Abb. 2.7.: Hybride Lokomotive Toshiba HD300 aus [Wik13]')
    2.7
    """
    splitted = german.word_tokenize(reference, validate_sentences=False)
    numbers = []
    for item in splitted:
        # convert possible Mark to str to use str operation
        item = str(item)
        # TODO: IMPROVE THIS APPROACH
        # enable converting int and float
        # cut last . in `2.7.`
        item = item[:-1] if item[-1] == '.' else item
        if not utila.isnumber(item):
            continue
        try:
            numbers.append(int(item))
        except ValueError:
            numbers.append(float(item))
    return numbers[0] if numbers else None

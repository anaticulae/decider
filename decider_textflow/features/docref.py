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
import konrad
import protocol
import serializeraw
import utila


def work(
        figure: str,
        section: str,
        table: str,
        caption_figure: str,
        caption_image: str,
        caption_table: str,
        text: str,
        headlines: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    figure = serializeraw.load_docref(figure, pages=pages)
    section = serializeraw.load_docref(section, pages=pages)
    table = serializeraw.load_docref(table, pages=pages)
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    text = serializeraw.load_text(text, headlines=headlines, pages=pages)
    caption_figure = serializeraw.load_captions(caption_figure, pages=pages)
    caption_image = serializeraw.load_captions(caption_image, pages=pages)
    caption_table = serializeraw.load_captions(caption_table, pages=pages)

    # prepare
    driver = protocol.driver(
        figure=figure,
        section=section,
        table=table,
        headlines=headlines,
        text=text,
        caption_figure=caption_figure,
        caption_image=caption_image,
        caption_table=caption_table,
    )

    # run
    linter = protocol.from_module(__name__)
    linter.run(driver=driver)

    # dump
    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


SOLUTION_7200 = """\
Referenz nicht gefunden

Der Abbildungs-Verweis **{{reference}}** kann nicht gefunden werden.
"""


def check_7200_figure_reference_exists(linter: callable, driver):
    captions = caption_numbers(driver.caption_figure + driver.caption_image)
    for reference in driver.figure:
        selected = determine_reference(reference, driver.text)
        if reference_exists(selected, captions):
            continue
        location = iamraw.RangedLocation(page=reference.page)
        raw = ', '.join(selected)
        linter(location=location, reference=raw)


SOLUTION_7202 = """\
Referenz nicht gefunden

Der Tabellen-Verweis **{{reference}}** kann nicht gefunden werden.
"""


def check_7202_table_reference_exists(linter: callable, driver):
    captions = caption_numbers(driver.caption_table)
    for reference in driver.table:
        selected = determine_reference(reference, driver.text)
        if reference_exists(selected, captions):
            continue
        location = iamraw.RangedLocation(page=reference.page)
        raw = ', '.join(selected)
        linter(location=location, reference=raw)


def determine_reference(item, text) -> str:
    selected = utila.select_content(text, page=item.page)
    marked = item.marked
    sentence_number = 0
    for section in selected:
        for sentence in section.content:
            if sentence_number == item.sentence:
                words = [
                    konrad.mark2str(item) for item in german.split_words(
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
    refnumber = {reference_number(item) for item in reference}
    diff = refnumber - captions
    # all references are linked if `diff` is empty
    return not diff


def reference_number(reference) -> int:
    """\
    >>> reference_number('Abbildung 10: Verschiebung des Order')
    10
    >>> reference_number('Abb. 2.7.: Hybride Lokomotive Toshiba HD300 aus [Wik13]')
    2.7
    """
    splitted = german.split_words(reference, validate_sentences=False)
    numbers = []
    for item in splitted:
        # TODO: IMPROVE THIS APPROACH
        # enable converting int and float
        # cut last . in `2.7.`
        item = item[:-1] if str(item)[-1] == '.' else item
        if not utila.isnumber(item):
            continue
        try:
            numbers.append(int(item))
        except ValueError:
            numbers.append(float(item))
    return numbers[0] if numbers else None

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import protocol
import serializeraw

import decider_smarty.utils


def work(
        invalid_prefix: str,
        phrases: str,
        pleonasms: str,
        text: str,
        headlines: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    # prepare findings
    invalid_prefix = serializeraw.load_docref(invalid_prefix, pages=pages)
    phrases = serializeraw.load_docref(phrases, pages=pages)
    pleonasms = serializeraw.load_docref(pleonasms, pages=pages)
    # content
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    text = serializeraw.load_text(text, headlines=headlines, pages=pages)
    # sentences
    sentences = decider_smarty.utils.sentence_lookup(text)
    # driver
    driver = protocol.driver(
        invalid_prefix=invalid_prefix,
        phrases=phrases,
        pleonasms=pleonasms,
        sentences=sentences,
        text=text,
    )
    # create and run
    linter = protocol.from_module(__name__)
    linter.run(driver=driver)
    # dump
    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


SOLUTION_8100 = """\
Umgangssprache erkannt

Vermeiden Sie **{{phrase}}** und ersetzen Sie diese durch eine \
förmlichere Formulierung.

TODO: ADD LINK
"""


def check_8100_non_formal_speach(linter: callable, driver):
    run_reference_results(linter, driver.sentences, driver.phrases)


SOLUTION_8105 = """\
Pleonasma erkannt

Vermeiden Sie **{{phrase}}** und reduzieren Sie diesen auf das \
Wesentliche.

TODO: ADD LINK
"""


def check_8105_pleonasms_detected(linter: callable, driver):
    run_reference_results(linter, driver.sentences, driver.pleonasms)


SOLUTION_8110 = """\
Unnötige Vorsible

Reduzieren Sie **{{phrase}}** indem Sie die unnötige Vorsilbe entfernen.

TODO: ADD LINK
"""


def check_8110_not_required_prefix(linter: callable, driver):
    run_reference_results(linter, driver.sentences, driver.invalid_prefix)


def run_reference_results(linter, text, errors):
    for error in errors:
        page, sentenceid, marked = error.page, error.sentence, error.marked
        sentences = decider_smarty.utils.sentence_plain(
            text[page][sentenceid],
            marks=marked,
        )
        for single in sentences:
            location = iamraw.Location.from_sentence(
                page=page,
                sentence=sentenceid,
            )
            linter(location=location, phrase=single)

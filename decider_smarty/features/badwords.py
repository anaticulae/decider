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

import decider_smarty.driver
import decider_smarty.utils


def work(
    invalid_prefix: str,
    phrases: str,
    pleonasms: str,
    text: str,
    headlines: str,
    pages: tuple = None,
) -> typing.Tuple[str, str]:
    driver = decider_smarty.driver.create(
        invalid_prefix,
        phrases,
        pleonasms,
        headlines,
        text,
        pages=pages,
    )
    result = protocol.run(
        modulename=__name__,
        driver=driver,
    )
    return result


SOLUTION_W8100 = """\
Umgangssprache erkannt

Vermeiden Sie **{{phrase}}** und ersetzen Sie diese durch eine \
förmlichere Formulierung.

{text/stilkunde/woerter/wortwahl}
"""


def check_8100_non_formal_speach(linter: callable, driver):
    run_reference_results(linter, driver.sentences, driver.phrases)


SOLUTION_W8105 = """\
Pleonasma erkannt

Vermeiden Sie **{{phrase}}** und reduzieren Sie diesen auf das \
Wesentliche.

{text/stilkunde/woerter/pleonasmen}
"""


def check_8105_pleonasms_detected(linter: callable, driver):
    run_reference_results(linter, driver.sentences, driver.pleonasms)


SOLUTION_W8110 = """\
Unnötige Vorsilbe

Reduzieren Sie **{{phrase}}** indem Sie die unnötige Vorsilbe entfernen.

TODO
"""


def check_8110_not_required_prefix(linter: callable, driver):
    run_reference_results(linter, driver.sentences, driver.invalid_prefix)


def run_reference_results(linter, text, errors):
    for error in errors:
        # TODO: REFACTOR LATER
        error = error.docref
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

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import typing

import iamraw
import protocol
import serializeraw

import decider_toc.duplicated as dtd
import decider_toc.marks


def work(tableofcontent: str) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)

    tableofcontent: iamraw.Toc = serializeraw.load_toc(tableofcontent)

    # run linter
    linting(tableofcontent, linter)

    result = linter.result(unique=False)

    # dump linter result
    user, developer = protocol.dump_result(result)
    return user, developer


TOC_CHECKER_ID = 13


def linting(toc, linter: protocol.Linter):
    location = iamraw.Location.from_page(1)
    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
            location=location,
        )
        checker(call, toc)


SOLUTION_1380 = """\
Worthäufung im Inhaltsverzeichnis

Das Wort „{{word}}“ wird {{count}} mal in den Zeilen {{lines}} benutzt.
Variieren Sie dieses Wort um die Varianz der Sprache zu vergrößern.
"""


def check_1380_toc_duplicated_words(linter, toc: iamraw.Toc):
    findings = dtd.validate(toc)
    for item in findings:
        (word, count), lines = item
        lines = ', '.join([f'{item}' for item in lines])
        # location = iamraw.Location.from_page(item.raw_location)
        linter(
            word=word,
            count=count,
            lines=lines,
        )


# TODO: ADD ARTICLE
SOLUTION_1383 = """\
Sektion enthält Fragestellung

Die Überschrift {{number}} „{{title}}“ ist als Frage formuliert.

Überschriften zeichnen sich durch Knappheit und Eindeutigkeit aus. Daher
sollten diese substantivisch, kurz und prägnant und nicht als Teilsatz oder
Fragesatz formuliert werden.
"""


def check_1383_toc_contains_question_mark(linter, toc: iamraw.Toc):
    findings = decider_toc.marks.validate_question_mark(toc)
    for item in findings:
        index, title, raw_location = item
        location = iamraw.Location.from_page(raw_location)
        linter(number=index, title=title, location=location)


# TODO: ADD ARTICLE
SOLUTION_1384 = """\
Sektion enthält Anführungszeichen

Die Überschrift {{number}} „{{title}}“ enhält Anführungszeichen. Dies
deutet auf eine spezielle Bedeutung hin. Dies sollte vermieden werden,
da Überschriften, kurz, prägnant und substantivisch formuliert sein sollen.

Überlegen Sie, wie die Sektion prägnanter und ohne spezielles Vorwissen
verständlich wird.
"""


def check_1384_toc_contains_quotation_mark(linter, toc: iamraw.Toc):
    findings = decider_toc.marks.collect_quotation_marks(toc)
    for item in findings:
        index, title, raw_location = item
        location = iamraw.Location.from_page(raw_location)
        linter(number=index, title=title, location=location)
        # TODO
        # assert 0

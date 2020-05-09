# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
""".. _decider_features_toc:

Table of content
================
"""
import functools
import typing

import iamraw
import protocol
import serializeraw

import decider.features
import decider.toc.duplicated as dtd
import decider.toc.length
import decider.toc.level as dtl
import decider.toc.marks
import decider.toc.pages as dtp


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


def linting(
        toc,
        linter: protocol.Linter,
):
    location = protocol.Location.from_page(1)
    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
            location=location,
        )
        checker(call, toc)


# TODO: ADD SOLUTION_1300_MS to link how to create table of content in word
# TODO: ADD SOLUTION_1300_LATEX to link how to create table of content in LATEX

SOLUTION_1300 = """\
Dokument enthält kein Inhaltsverzeichnis

Fügen Sie ein Inhaltsverzeichnis zum Dokument hinzu.

TODO: ADD LINK TO TECHNIK

{elemente/inhaltsverzeichnis}
"""


def check_1300_toc_existence(linter, toc: iamraw.Toc):
    if toc.children:
        return
    linter(location=decider.features.OVERVIEW)


SOLUTION_1350 = """\
Kapitel enthält zu wenige Sektionen

Ein Kapitel oder eine Sektion benötigt mindestens zwei
Teilüberschriften. Falls dies nicht moeglich ist, sollte das
Unterkapitel in den Text eingeplegt werden.

{elemente/inhaltsverzeichnis#kapitelstruktur}
"""


def check_1350_toc_level_to_few_children(linter, toc: iamraw.Toc):
    level_result: dtl.TocValidationResult = dtl.validate(toc)
    for item in level_result.too_few_children:  # pylint:disable=E1133
        # TODO: REMOVE AFTER UPGRADING SERIALIZERAW
        location = protocol.Location.from_page(int(item.page))
        linter(location=location)


SOLUTION_1351 = """
Gliederung zu komplex

Das Dokument weist eine zu detaillierte Untergliederung auf. Eine zu
feingliedrige Gliederung reduziert die Üebersichtlichkeit und verhindert
das schnelle Navigieren im Text.

Begrenzen Sie die Gliederung auf maximal 3 Sektionen.

{elemente/inhaltsverzeichnis#tiefe-der-gliederung}
"""


def check_1351_toc_level_to_deep(linter, toc: iamraw.Toc):
    level_result: dtl.TocValidationResult = dtl.validate(toc)
    for item in level_result.level_to_deep:  # pylint:disable=E1133
        # TODO: REMOVE AFTER UPGRADING SERIALIZERAW
        location = protocol.Location.from_page(int(item.page))
        linter(location=location)


SOLUTION_1360 = """\
Inhaltsverzeichnis enthält nicht nur aufsteigende Seitenzahlen

Korrigieren Sie das Inhaltsverzeichnis bzw. die Seitenzahlen.

Zeile: {%text%}
Seite {%current%} folgt auf {%before%}.

{darstellung/seitenzahlen#anforderungen}
"""


def check_1360_toc_ascending_pages(linter, toc: iamraw.Toc):
    page_result: dtp.InvalidPages = dtp.validate(toc)
    for item in page_result:
        location = protocol.Location.from_page(item.raw_location)
        linter(
            current=item.current,
            before=item.before,
            text=item.text,
            location=location,
        )


SOLUTION_1380 = """\
Worthäufung im Inhaltsverzeichnis

Das Wort „{%word%}“ wird {%count%} mal in den Zeilen {%lines%} benutzt.
Variieren Sie dieses Wort um die Varianz der Sprache zu vergrößern.
"""


def check_1380_toc_duplicated_words(linter, toc: iamraw.Toc):
    findings = dtd.validate(toc)
    for item in findings:
        (word, count), lines = item
        lines = ', '.join([f'{item}' for item in lines])
        # location = protocol.Location.from_page(item.raw_location)
        linter(
            word=word,
            count=count,
            lines=lines,
        )


# TODO: Link to article
# TODO: Convert citation marks
SOLUTION_1382 = """\
Überschrift zu lang

Die Überschrift {%number%} „{%title%}“ ist zu lang und verkürzt werdne.
"""


def check_1382_toc_long_lines(linter, toc: iamraw.Toc):
    findings = decider.toc.length.validate(toc)
    for item in findings:
        index, title, _, raw_location = item
        location = protocol.Location.from_page(raw_location)
        linter(number=index, title=title, location=location)


# TODO: ADD ARTICLE
SOLUTION_1383 = """\
Sektion enthält Fragestellung

Die Überschrift {%number%} „{%title%}“ ist als Frage formuliert.

Überschriften zeichnen sich durch Knappheit und Eindeutigkeit aus. Daher
sollten diese substantivisch, kurz und prägnant und nicht als Teilsatz oder
Fragesatz formuliert werden.
"""


def check_1383_toc_contains_question_mark(linter, toc: iamraw.Toc):
    findings = decider.toc.marks.validate_question_mark(toc)
    for item in findings:
        index, title, raw_location = item
        location = protocol.Location.from_page(raw_location)
        linter(number=index, title=title, location=location)

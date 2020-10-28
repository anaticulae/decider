# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import typing

import iamraw
import protocol
import serializeraw
import utila

import decider_toc.balance
import decider_toc.length
import decider_toc.level as dtl
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


SOLUTION_1351 = """\
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
        location = iamraw.Location.from_page(int(item.page))
        linter(location=location)


SOLUTION_1370 = """\
Abschnitt zu lang

Der Abschnitt „{{headline}}“ ist im Vergleich zu den gleichranggigen
Abschnitten({{expected}}) zu lang({{current}}). Überdenken Sie die
Abschnittseinteilung und überlegen Sie sich weitere Teilabschnitte
einzuführen.

{aufbau_gliederung/absatz}
"""


def check_1370_section_too_long(linter, toc: iamraw.Toc):
    validate_chapter_length(
        linter,
        toc,
        level=2,
        expected=decider_toc.balance.TOO_LONG,
    )

    validate_chapter_length(
        linter,
        toc,
        level=3,
        expected=decider_toc.balance.TOO_LONG,
    )


SOLUTION_1371 = """\
Abschnitt zu kurz

Der Abschnitt „{{headline}}“ ist im Vergleich zu den gleichranggigen
Abschnitten({{expected}}) zu kurz({{current}}). Überdenken Sie die
Abschnittseinteilung und überlegen Sie sich Teilabschnitte zusammen zu
führen.

{aufbau_gliederung/absatz}
"""


def check_1371_section_too_short(linter, toc: iamraw.Toc):
    validate_chapter_length(
        linter,
        toc,
        level=2,
        expected=decider_toc.balance.TOO_SHORT,
    )
    validate_chapter_length(
        linter,
        toc,
        level=3,
        expected=decider_toc.balance.TOO_SHORT,
    )


def validate_chapter_length(linter, toc, level, expected):
    balanced = decider_toc.balance.judge(toc)
    level2 = utila.flatten(balanced.level2)
    flat = decider_toc.balance.data(toc)

    level_two = [item for item in flat if item.level == level]

    for line, judged in zip(level_two, level2):
        if judged[0] != expected:
            continue
        title = line.title
        location = iamraw.Location.from_page(line.page)
        linter(
            location=location,
            headline=title,
            current=judged[1],
            expected=judged[2],
        )


# TODO: Link to article
# TODO: Convert citation marks
SOLUTION_1382 = """\
Überschrift zu lang

Die Überschrift {{number}} „{{title}}“ ist zu lang und sollte verkürzt
werden.
"""


def check_1382_toc_long_lines(linter, toc: iamraw.Toc):
    findings = decider_toc.length.validate(toc)
    for item in findings:
        index, title, _, raw_location = item
        location = iamraw.Location.from_page(raw_location)
        linter(number=index, title=title, location=location)

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
    location = protocol.Location.from_page(1)
    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
            location=location,
        )
        checker(call, toc)


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


# TODO: Link to article
# TODO: Convert citation marks
SOLUTION_1382 = """\
Überschrift zu lang

Die Überschrift {%number%} „{%title%}“ ist zu lang und verkürzt werdne.
"""


def check_1382_toc_long_lines(linter, toc: iamraw.Toc):
    findings = decider_toc.length.validate(toc)
    for item in findings:
        index, title, _, raw_location = item
        location = protocol.Location.from_page(raw_location)
        linter(number=index, title=title, location=location)

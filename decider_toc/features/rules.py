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

import decider_toc.level as dtl
import decider_toc.pages as dtp


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

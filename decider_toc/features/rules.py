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

import decider_toc.level as dtl
import decider_toc.pages as dtp
import decider_toc.utils


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
        try:
            location = iamraw.Location.from_page(int(item.page))
        except ValueError:
            # TODO: THINK ABOUT CONCEPT TO HANDLE ROMAN PAGE NUMBERS
            # TODO: INTRODUCE RAW LOCATION?
            utila.error(f'could not convert roman page number: {item.page}')
            continue
        linter(location=location)


SOLUTION_1360 = """\
Inhaltsverzeichnis enthält nicht nur aufsteigende Seitenzahlen

Korrigieren Sie das Inhaltsverzeichnis bzw. die Seitenzahlen.

Zeile: {{text}}
Seite {{current}} folgt auf {{before}}.

{darstellung/seitenzahlen#anforderungen}
"""


def check_1360_toc_ascending_pages(linter, toc: iamraw.Toc):
    page_result: dtp.InvalidPages = dtp.validate(toc)
    for item in page_result:
        location = iamraw.Location.from_page(item.raw_location)
        linter(
            current=item.current,
            before=item.before,
            text=item.text,
            location=location,
        )


SOLUTION_1365 = """\
Eidesstattliche Erklärung als Teil der Arbeit

Die Eidesstatttliche Erklärung ist kein Teil der Prüfungsleistung und
wird somit nicht im Inhaltsverzeichnis aufgeführt und wird ebenfalls
nicht bei der Seitenzählung berücksichtigt.

{elemente/erklaerung}
"""

# TODO: MOVE TO KONRAD?
# TODO: ADD METHOD WHICH CAN JUDGE TYPOS TOO
# TODO: LOWER
LEGAL = set(item.lower() for item in [
    'Eidesstattliche Erklärung',
    'Eidesstattliche Versicherung',
])


def islegal(item: str) -> bool:
    item = item.strip().lower()
    return item in LEGAL


def check_1365_toc_legal_inside_toc(linter, toc: iamraw.Toc):
    if not toc:
        return
    toc = decider_toc.utils.flat(toc)

    legal_intoc = [item for item in toc if islegal(item.title)]
    if not legal_intoc:
        return

    location = iamraw.Location.from_page(legal_intoc[0].raw_location)
    linter(location=location)

    if len(legal_intoc) >= 2:
        utila.error(f'multiple legal toc detected {legal_intoc}')

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
import yaml

import decider.toc.level as dtl
import decider.toc.pages as dtp
import decider.utils


def work(tableofcontent: str) -> typing.Tuple[str, str]:
    linter = decider.utils.from_module(__name__)

    tableofcontent: iamraw.Toc = serializeraw.load_toc(tableofcontent)

    # run linter
    linting(tableofcontent, linter)

    result = linter.result(unique=False)

    # dump linter result
    user_dumped = yaml.dump(result[0])
    developer_dumped = yaml.dump(result[1])
    return user_dumped, developer_dumped


TOC_CHECKER_ID = 13


def linting(
        toc,
        linter: protocol.Linter,
):
    location = protocol.Location.from_page(1)
    checkers = decider.utils.parse_checkers(__name__)
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
Dokument enhaelt kein Inhaltsverzeichnis

Fuegen Sie ein Inhaltsverzeichnis zum Dokument hinzu.
"""


def check_1300_toc_existence(linter, toc: iamraw.Toc):
    if toc.children:
        return
    linter()


SOLUTION_1350 = """\
Kapitel enthaelt zu wenige Sektionen

Ein Kapitel oder eine Sektion benoetigt mindestens zwei
Teilueberschriften. Falls dies nicht moeglich ist, sollte das
Unterkapitel in den Text eingeplfegt werden.
"""


def check_1350_toc_level_to_few_children(linter, toc: iamraw.Toc):
    level_result: dtl.TocValidationResult = dtl.validate(toc)
    for _ in level_result.too_few_children:  # pylint:disable=E1133
        linter()


SOLUTION_1351 = """
Der Unterpunkt weist eine zu tiefe Gliederung auf

Das Dokument weist eine zu detaillierte Untergliederung auf. Eine zu
feingliedrige Gliederung reduziert die Uebersichtlichkeit und verhindert
das schnelle Navigieren im Text.

Begrenzen Sie die Gliederung auf maximal 3 Sektionen.
"""


def check_1351_toc_level_to_deep(linter, toc: iamraw.Toc):
    level_result: dtl.TocValidationResult = dtl.validate(toc)
    for _ in level_result.level_to_deep:  # pylint:disable=E1133
        linter()


SOLUTION_1360 = """\
Das Inhaltsverzeichnis enthaellt nicht nur aufsteigende Seitenzahlen

Korrigieren Sie das Inhaltsverzeichnis.

Zeile: {%text%}

Seite {%current%} folgt auf {%before%}.
"""


def check_1360_toc_ascending_pages(linter, toc: iamraw.Toc):
    if not toc:
        return
    page_result: dtp.InvalidPages = dtp.validate(toc)
    for item in page_result:
        linter(current=item.current, before=item.before, text=item.text)

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Sync
====

TOC - Outlines
TOC - Content

Verify:
    - level
    - text
    - page number
"""

import functools
import typing

import iamraw
import protocol
import serializeraw
import utila

import decider.features

# TODO: ADD SOLUTION TO COMPARE TOC AND OUTLINES


def work(
        tableofcontent: str,
        outlines: str,
        headlines: str,
) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)

    tableofcontent: iamraw.Toc = serializeraw.load_toc(tableofcontent)
    outlines = serializeraw.load_toc(outlines)
    headlines = serializeraw.load_headlines(headlines)

    driver = protocol.driver(
        toc=tableofcontent,
        outlines=outlines,
        headlines=headlines,
    )

    # run linter
    linting(driver, linter)

    result = linter.result(unique=False)

    # dump linter result
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(driver, linter: protocol.Linter):
    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
        )
        checker(call, driver)


SOLUTION_1330 = """\
Inhaltsverzeichnis nicht aktuell

Die im Inhaltsverzeichnis verzeichneten Kapitelüberschriften weichen von
dem im Dokument enthaltenen Überschriften ab. Akutallisieren Sie das
Inhaltsverzeichnis.

Folgende Überschriften sind nicht im Inhaltsverzeichnis enthalten:

{%missing%}
"""


def check_1330_toc_document_sync(linter, driver):
    toc = driver.toc
    if not toc:
        utila.error('no toc')
        return
    headlines = driver.headlines
    if not headlines:
        utila.error('no headlines given')
        return
    headlines = iamraw.headlines_totoc(headlines)

    # compare first level
    toc_first_level = [item.title for item in toc]
    document_first_level = [item.title for item in headlines]

    if toc_first_level == document_first_level:
        # all first level headlines in toc are equal to detected headlines
        # in document
        return
    # TODO: ADD LEVEL AND PAGE TO EASE LOCATING HEADLINE
    # TODO: ADD MISSING IN DOCUMENT
    missing = [
        item for item in document_first_level if item not in toc_first_level
    ]
    missing = utila.NEWLINE.join([f'* {item}' for item in missing])
    linter(location=decider.features.OVERVIEW, missing=missing)


# def check_1335_toc_outlines_sync(linter, driver):
#     pass

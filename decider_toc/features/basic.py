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

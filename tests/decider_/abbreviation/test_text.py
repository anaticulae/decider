# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import iamraw
import protocol
import utila

import decider.features.abbreviation_text as dfa

TABLE = iamraw.AbbreviationResult(abbreviations=[
    iamraw.Abbreviation(
        short='SCB',
        description='Soli Chobi Bobi',
    ),
    iamraw.Abbreviation(
        short='WAL',
        description='Word Aliance Lord',
    ),
])

EXAMPLE = [
    iamraw.ExtractedTextAbbreviation(
        page=2,
        content=[
            iamraw.Abbreviation(
                short='SCB',
                position=iamraw.AbbreviationPosition(
                    page=2,
                    sentence=1,
                ),
            ),
            iamraw.Abbreviation(
                short='WAL',
                position=iamraw.AbbreviationPosition(
                    page=2,
                    sentence=2,
                ),
            ),
            iamraw.Abbreviation(
                short='WAL',
                description='Word Aliance Lord',
                position=iamraw.AbbreviationPosition(
                    page=2,
                    sentence=10,
                ),
            ),
        ]),
]


def abbreviation_linter(method):
    linter = protocol.from_module(dfa)
    location = protocol.Location.from_page(2)
    msgid = vars(method)['msgid']
    call = functools.partial(
        linter.add_finding,
        msgid=msgid,
        location=location,
    )
    linter.add_finding = call
    return linter


def test_linter_abbreviation_text_before_used():
    check_before_used = dfa.check_5100_used_before_defined
    linter = abbreviation_linter(check_before_used)
    check_before_used(
        linter.add_finding,
        table=TABLE,
        text=EXAMPLE,
    )
    assert linter.findings, str(linter.findings)
    assert len(linter.findings) == 1

    expected_msgid = protocol.parse_msgid(check_before_used.__name__)
    msgid = linter.findings[0].msgid
    description = linter.findings[0].solution.description
    assert msgid == expected_msgid
    assert utila.istemplate_replaced(description), description

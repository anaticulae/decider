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

import decider.features.abbreviation_table
import tests


def test_linter_abbreviation_table_sorted():
    table = iamraw.AbbreviationResult()
    for item in ['Alpha', 'Beta', 'Gamma', 'helm']:
        table.append(iamraw.Abbreviation(item))

    linter = protocol.Linter()
    decider.features.abbreviation_table.check_5000_not_sorted_alphabetically(
        linter.add_finding,
        table,
    )
    assert linter.findings == []


def abbreviation_linter(method):
    linter = protocol.from_module(decider.features.abbreviation_table)
    location = protocol.Location.from_page(5)
    msgid = vars(method)['msgid']
    call = functools.partial(
        linter.add_finding,
        msgid=msgid,
        location=location,
    )
    linter.add_finding = call
    return linter


EXAMPLE = [
    ('Beta', 'Dies ist ein Parmeter'),
    ('Alpha', 'Dies ist noch ein Parmeter'),
    ('helm', 'H * l * m * n'),
    ('Gamma', 'require more'),
]


def test_linter_abbreviation_table_unsorted():
    table = iamraw.AbbreviationResult()
    for short, description in EXAMPLE:
        table.append(
            iamraw.Abbreviation(
                short=short,
                description=description,
            ))

    linter = abbreviation_linter(decider.features.abbreviation_table.
                                 check_5000_not_sorted_alphabetically)
    decider.features.abbreviation_table.check_5000_not_sorted_alphabetically(
        linter.add_finding,
        table,
    )
    assert len(linter.findings) == 1, str(linter.findings)

    description = linter.findings[0].solution.description
    assert tests.template_replaced(description), description

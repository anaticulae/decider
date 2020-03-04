# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import groupme.abbreviation
import protocol
import pytest
import utila

import decider.features.abbreviation_table
import tests
import tests.resources


@pytest.mark.parametrize('source, pages', [
    pytest.param(
        tests.resources.BACHELOR37_GENERATED,
        '1',
        id='bachelor37',
    ),
])
def test_cli_groupme_abbreviation_table(source, pages, testdir, monkeypatch):
    """Run decider"""
    root = testdir.tmpdir
    cmd = f'groupme -i {source} -o {root} --abbreviation --pages={pages}'
    completed = utila.run(cmd)
    assert completed.returncode == utila.SUCCESS, str(completed)

    cmd = f'-i {root} -i {source} -o {root} --abbreviation'
    tests.run_decider(cmd, monkeypatch)


def test_linter_abbreviation_table_sorted():
    table = groupme.abbreviation.AbbreviationResult()
    for item in ['Alpha', 'Beta', 'Gamma', 'helm']:
        table.append(groupme.abbreviation.Abbreviation(item))

    linter = protocol.Linter()
    decider.features.abbreviation_table.check_5000_not_sorted_alphabetically(
        table,
        linter.add_finding,
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
    table = groupme.abbreviation.AbbreviationResult()
    for short, description in EXAMPLE:
        table.append(
            groupme.abbreviation.Abbreviation(
                short=short,
                description=description,
            ))

    linter = abbreviation_linter(decider.features.abbreviation_table.
                                 check_5000_not_sorted_alphabetically)
    decider.features.abbreviation_table.check_5000_not_sorted_alphabetically(
        table,
        linter.add_finding,
    )
    assert len(linter.findings) == 1, str(linter.findings)
    description = linter.findings[0].solution.description
    # TODO: REPLACE WITH MORE GENERAL METHOD
    # template is replaced correctly
    assert '%' not in description, description
    assert '[' not in description, description
    assert '(' not in description, description

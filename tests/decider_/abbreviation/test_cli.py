# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila

import tests.resources


@pytest.mark.parametrize('source, pages', [
    pytest.param(
        tests.resources.BACHELOR37,
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

    cmd = f'-i {root} -i {source} -o {root} --abbreviation_table'
    tests.run_decider(cmd, monkeypatch)


@pytest.mark.parametrize('source, pages', [
    pytest.param(
        tests.resources.BACHELOR37,
        '1',
        id='bachelor37',
    ),
])
def test_cli_groupme_abbreviation_text(source, pages, testdir, monkeypatch):
    """Run decider"""
    root = testdir.tmpdir
    cmd = f'groupme -i {source} -o {root} --abbreviation --pages={pages}'
    completed = utila.run(cmd)
    assert completed.returncode == utila.SUCCESS, str(completed)

    cmd = f'-i {root} -i {source} -o {root} --abbreviation_text'
    tests.run_decider(cmd, monkeypatch)

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila
import utilatest

import tests
import tests.resources


@pytest.mark.parametrize('cmd', [
    '--help',
])
def test_cli_decider(cmd, testdir, monkeypatch):
    """Run decider"""
    tests.run_decider(cmd, monkeypatch=monkeypatch)


@pytest.mark.parametrize('source', [
    pytest.param(tests.resources.BACHELOR37, id='bachelor37'),
    pytest.param(tests.resources.BACHELOR76, id='bachelor76'),
    pytest.param(tests.resources.DOCU_TWINE, id='docu'),
    pytest.param(tests.resources.LEFTRIGHT, id='leftright'),
    pytest.param(tests.resources.MASTER72, id='master72'),
    pytest.param(tests.resources.MASTER78, id='master78'),
    pytest.param(tests.resources.MASTER98, id='master98'),
    pytest.param(tests.resources.MASTER99, id='master99'),
])
def test_cli_decider_example(source, testdir, monkeypatch):
    """Run decider"""
    cmd = f'-i {source}'
    tests.run_decider(cmd, monkeypatch=monkeypatch)


@pytest.mark.parametrize('source, pages', [
    pytest.param(
        tests.resources.TECHNICAL24,
        '1',
        id='technical24',
    ),
    pytest.param(
        tests.resources.TECHNICAL24,
        '0:5',
        id='technical24',
    ),
    pytest.param(
        tests.resources.MASTER78,
        '0:5',
        id='master78',
    ),
    pytest.param(
        tests.resources.MASTER72,
        '0:5',
        id='master72',
    ),
])
@utilatest.skip_longrun
def test_cli_detector_and_decider(source, pages, testdir, monkeypatch):
    """Run decider

    pages = 1 - Non titlepage example
    """
    root = str(testdir)
    cmd = f'detector -i {source} -o {root} --pages={pages}'
    completed = utila.run(cmd)
    assert completed.returncode == utila.SUCCESS, str(completed)

    cmd = f'-i {root} -i {source} -o {root}'
    tests.run_decider(cmd, monkeypatch)

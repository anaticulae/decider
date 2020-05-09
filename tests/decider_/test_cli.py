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

import tests
import tests.resources


@pytest.mark.parametrize('cmd', [
    '--help',
])
def test_cli_decider(cmd, testdir, monkeypatch):
    """Run decider"""
    tests.run_decider(cmd, monkeypatch=monkeypatch)


# yapf:disable
@pytest.mark.parametrize('source', [
    pytest.param(tests.resources.BACHELOR37_GENERATED, id='bachelor37'),
    pytest.param(tests.resources.BACHELOR76_GENERATED, id='bachelor76', marks=pytest.mark.xfail(reason='none int page')),
    pytest.param(tests.resources.DOCU_TWINE_GENERATED, id='docu'),
    pytest.param(tests.resources.LEFTRIGHT_GENERATED, id='leftright'),
    pytest.param(tests.resources.MASTER72_GENERATED, id='master72'),
    pytest.param(tests.resources.MASTER78_GENERATED, id='master78'),
    pytest.param(tests.resources.MASTER98_GENERATED, id='master98'),
    pytest.param(tests.resources.MASTER99_GENERATED, id='master99'),
])
# yapf:enable
def test_cli_decider_example(source, testdir, monkeypatch):
    """Run decider"""
    cmd = f'-i {source}'
    tests.run_decider(cmd, monkeypatch=monkeypatch)


@pytest.mark.parametrize('source, pages', [
    pytest.param(
        tests.resources.TECHNICAL24_GENERATED,
        '1',
        id='technical24',
    ),
    pytest.param(
        tests.resources.TECHNICAL24_GENERATED,
        '0:5',
        id='technical24',
    ),
    pytest.param(
        tests.resources.MASTER78_GENERATED,
        '0:5',
        id='master78',
    ),
    pytest.param(
        tests.resources.MASTER72_GENERATED,
        '0:5',
        id='master72',
    ),
])
@utila.skip_longrun
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

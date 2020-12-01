# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import tests


@pytest.mark.parametrize('cmd', [
    '--help',
])
def test_cli_decider(cmd, testdir, monkeypatch):
    """Run decider"""
    tests.run_decider(cmd, monkeypatch=monkeypatch)


@pytest.mark.parametrize('source', [
    pytest.param(power.link(power.BACHELOR037_PDF), id='bachelor37'),
    pytest.param(power.link(power.BACHELOR076_PDF), id='bachelor76'),
    pytest.param(power.link(power.DOCU35_PDF), id='docu'),
    pytest.param(power.link(power.BOOK007_PDF), id='leftright'),
    pytest.param(power.link(power.MASTER072_PDF), id='master72'),
    pytest.param(power.link(power.MASTER078_PDF), id='master78'),
    pytest.param(power.link(power.MASTER098_PDF), id='master98'),
    pytest.param(power.link(power.MASTER099_PDF), id='master99'),
])
@utilatest.nightly
def test_cli_decider_example(source, testdir, monkeypatch):
    """Run decider"""
    cmd = f'-i {source}'
    tests.run_decider(cmd, monkeypatch=monkeypatch)


@pytest.mark.parametrize('source, pages', [
    pytest.param(
        power.link(power.TECH024_PDF),
        '1',
        id='technical24',
    ),
    pytest.param(
        power.link(power.TECH024_PDF),
        '0:5',
        id='technical24',
    ),
    pytest.param(
        power.link(power.MASTER078_PDF),
        '0:5',
        id='master78',
    ),
    pytest.param(
        power.link(power.MASTER072_PDF),
        '0:5',
        id='master72',
    ),
])
@utilatest.nightly
def test_cli_detector_and_decider(source, pages, testdir, monkeypatch):
    """Run decider

    pages = 1 - Non titlepage example
    """
    cmd = f'detector -i {source} -o {testdir.tmpdir} --pages={pages}'
    completed = utila.run(cmd)
    assert completed.returncode == utila.SUCCESS, str(completed)

    cmd = f'-i {testdir.tmpdir} -i {source} -o {testdir.tmpdir}'
    tests.run_decider(cmd, monkeypatch)

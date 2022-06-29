# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import tests


def test_cli_decider_help(monkeypatch):
    """Run help decider"""
    tests.run('--help', monkeypatch=monkeypatch)


@pytest.mark.parametrize('source', [
    pytest.param(power.BACHELOR037_PDF, id='bachelor37'),
    pytest.param(power.BACHELOR076_PDF, id='bachelor76'),
    pytest.param(power.DOCU035_PDF, id='docu'),
    pytest.param(power.BOOK007_PDF, id='leftright'),
    pytest.param(power.MASTER072_PDF, id='master72'),
    pytest.param(power.MASTER078_PDF, id='master78'),
    pytest.param(power.MASTER098_PDF, id='master98'),
    pytest.param(power.MASTER099_PDF, id='master99'),
])
@utilatest.nightly
def test_cli_decider_example(source, testdir, monkeypatch):
    """Run decider"""
    source = power.link(source)
    cmd = f'-i {source}'
    tests.run(cmd, monkeypatch=monkeypatch)


@pytest.mark.parametrize('source, pages', [
    pytest.param(power.TECH024_PDF, '1', id='technical24'),
    pytest.param(power.TECH024_PDF, '0:5', id='technical24'),
    pytest.param(power.MASTER078_PDF, '0:5', id='master78'),
    pytest.param(power.MASTER072_PDF, '0:5', id='master72'),
])
@utilatest.nightly
def test_cli_detector_and_decider(source, pages, testdir, monkeypatch):
    """Run decider

    pages = 1 - Non titlepage example
    """
    source = power.link(source)
    cmd = f'detector -i {source} -o {testdir.tmpdir} --pages={pages}'
    completed = utila.run(cmd)
    assert completed.returncode == utila.SUCCESS, str(completed)
    cmd = f'-i {testdir.tmpdir} -i {source} -o {testdir.tmpdir}'
    tests.run(cmd, monkeypatch=monkeypatch)

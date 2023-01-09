# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import tests


def test_cli_decider_help(mp):
    """Run help decider"""
    tests.run('--help', mp=mp)


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
def test_cli_decider_example(source, td, mp):  # pylint:disable=W0613
    """Run decider"""
    utilatest.fixture_requires(source)
    source = power.link(source)
    cmd = f'-i {source}'
    tests.run(cmd, mp=mp)


@pytest.mark.parametrize('source, pages', [
    pytest.param(power.TECH024_PDF, '1', id='technical24'),
    pytest.param(power.TECH024_PDF, '0:5', id='technical24'),
    pytest.param(power.MASTER078_PDF, '0:5', id='master78'),
    pytest.param(power.MASTER072_PDF, '0:5', id='master72'),
])
@utilatest.nightly
def test_cli_detector_and_decider(source, pages, td, mp):
    """Run decider

    pages = 1 - Non titlepage example
    """
    utilatest.fixture_requires(source)
    source = power.link(source)
    cmd = f'detector -i {source} -o {td.tmpdir} --pages={pages}'
    completed = utila.run(cmd)
    assert completed.returncode == utila.SUCCESS, str(completed)
    cmd = f'-i {td.tmpdir} -i {source} -o {td.tmpdir}'
    tests.run(cmd, mp=mp)

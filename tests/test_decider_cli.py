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

import decider
import tests.resources


@pytest.mark.parametrize('cmd', [
    '--help',
])
def test_cli_decider(cmd, testdir, monkeypatch):
    """Run decider"""
    utila.run_command(
        cmd,
        process=decider.PROCESS,
        main=decider.cli.main,
        monkeypatch=monkeypatch,
        success=True,
    )


@pytest.mark.parametrize('source', [
    pytest.param(
        tests.resources.TECHNICAL_24PAGES_GENERATED,
        id='technical24',
    ),
    pytest.param(
        tests.resources.MASTER_78_PAGES_IMAGES_GENERATED,
        id='master78',
    ),
    pytest.param(
        tests.resources.MASTER_72_PAGES_NOIMAGES_GENERATED,
        id='master72',
    ),
])
@utila.skip_longrun
def test_cli_detector_and_decider(source, testdir):
    """Run decider"""
    root = str(testdir)
    cmd = f'detector -i {source} -o {root}'
    completed = utila.run(cmd)
    assert completed.returncode == utila.SUCCESS, str(completed)

    cmd = f'decider -i {root} -i {source} -o {root}'
    completed = utila.run(cmd)
    assert completed.returncode == utila.SUCCESS, str(completed)

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utila
from detector.feature.title import RAWMAKER_CONFIGURATION

import decider
import tests
from tests.resources import MASTER_HUGE


@pytest.fixture
def titlepage(testdir):
    root = str(testdir)

    cmd = f'rawmaker -i {MASTER_HUGE} -o {root} {RAWMAKER_CONFIGURATION} --page=0'
    rawmaker__ = utila.run(cmd)
    assert rawmaker__.returncode == utila.SUCCESS, str(rawmaker__)
    cmd = f'detector -i {root} -o {root}'
    detector__ = utila.run(cmd)
    assert detector__.returncode == utila.SUCCESS, str(detector__)
    return root


def test_titlepage_extraction(titlepage, monkeypatch):  # pylint:disable=W0621
    root = str(titlepage)

    result = os.path.join(root, 'result')
    todo = f'--{decider.cli.TITLEPAGE}'
    cmd = f'-i {root} -o {result} {todo}'

    tests.run_decider(cmd, monkeypatch)

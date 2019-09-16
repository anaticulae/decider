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
import yaml

import decider
import decider.features.titlepage
import detector.feature.titlepage
import tests
import tests.resources


@pytest.fixture(
    params=[
        # (tests.resources.MASTER_HUGE, [
        #     decider.features.titlepage.MISSING_THESIS_TYPE_ID,
        # ]),
        (tests.resources.MASTER_72PAGES_NOIMAGES, [
            decider.features.titlepage.MISSING_AUTHOR_MATRIKEL_ID,
        ]),
    ],
    ids=[
        # 'MASTER_HUGE',
        'MASTER_72PAGES',
    ])
def titlepage(request, testdir):
    root = str(testdir)
    source, expected_failures = request.param
    cmd = (f'rawmaker -i {source} -o {root} --page=0 '
           f'{detector.feature.titlepage.RAWMAKER_CONFIGURATION}')
    rawmaker__ = utila.run(cmd)
    assert rawmaker__.returncode == utila.SUCCESS, str(rawmaker__)
    cmd = f'detector -i {root} -o {root}'
    detector__ = utila.run(cmd)
    assert detector__.returncode == utila.SUCCESS, str(detector__)
    return root, expected_failures


def test_titlepage_extraction(titlepage, monkeypatch):  # pylint:disable=W0621
    root, expected_failures = titlepage

    result = os.path.join(root, 'result')
    todo = f'--{decider.cli.TITLEPAGE}'
    cmd = f'-i {root} -o {result} {todo}'

    tests.run_decider(cmd, monkeypatch)

    userpath = os.path.join(result, decider.cli.USER_LINT_OUTPUT)
    user = yaml.load(utila.file_read(userpath), Loader=yaml.FullLoader)

    failures = messageids(user)

    assert failures == expected_failures, str(failures)


def messageids(items):
    result = [item.msgid for item in items]
    return result

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
import tests
import tests.resources


@pytest.fixture(
    params=[
        (tests.resources.MASTER116, [
            1210,
        ]),
        (tests.resources.MASTER72, [
            1221,
        ]),
        (tests.resources.MASTER78, []),
        (tests.resources.TWINE_NO_TITLE_PAGE, [
            1200,
        ]),
    ],
    ids=[
        'master116',
        'master72',
        'master78',
        'twine_no_title',
    ])
def titlepage(request, testdir):
    root = str(testdir)
    source, expected_failures = request.param

    # TODO: REMOVE PAGE SHRINKES AFTER FIXING BUG WITH DETECTION
    cmd = f'detector -i {source} -o {root} --pages=0'
    completed = utila.run(cmd)
    assert completed.returncode == utila.SUCCESS, str(completed)
    return root, expected_failures


@utila.skip_longrun
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

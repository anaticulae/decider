# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import pytest
import serializeraw
import utila
import utilatest

import decider
import decider.features.titlepage
import tests


@pytest.fixture(
    params=[
        (power.link(power.MASTER116_PDF), [
            1210,
        ]),
        (power.link(power.MASTER072_PDF), [
            1221,
        ]),
        (power.link(power.MASTER078_PDF), []),
        (power.link(power.DOCU35_PDF, folder='notitle'), [
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

    cmd = f'detector -i {source} -o {root}'
    completed = utila.run(cmd)
    assert completed.returncode == utila.SUCCESS, str(completed)
    return root, expected_failures


@utilatest.nightly
def test_titlepage_extraction(titlepage, monkeypatch):  # pylint:disable=W0621
    root, expected_failures = titlepage

    result = os.path.join(root, 'result')
    todo = f'--{decider.cli.TITLEPAGE}'
    cmd = f'-i {root} -o {result} {todo}'

    tests.run_decider(cmd, monkeypatch)

    userpath = os.path.join(result, decider.cli.USER_LINT_OUTPUT)
    user = serializeraw.load_findings(userpath)

    failures = [item.msgid for item in user]
    assert failures == expected_failures, str(failures)

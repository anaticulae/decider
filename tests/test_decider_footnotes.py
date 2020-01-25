# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import pytest
import utila

import decider.footnotes
import tests.resources


@pytest.fixture
def example():
    loaded = decider.footnotes.load(
        tests.resources.MASTER_72_PAGES_NOIMAGES_GENERATED,
        pages=(3),
    )
    return loaded[0]


def test_decider_footnotes_example(example):  # pylint:disable=W0621
    assert example.page == 3
    assert len(example.content) == 6


def test_decider_footnotes_validate(example):  # pylint:disable=W0621
    result = [decider.footnotes.validate(item) for item in example.content]

    valid = [item.valid for item in result]

    expected = [True, False, False, False, False, False]
    assert valid == expected


def test_decider_cli_footnotes(testdir, monkeypatch):  ## pylint:disable=W0621
    root = str(testdir)

    cmd = ['-i', tests.resources.MASTER_72_PAGES_NOIMAGES_GENERATED, '-o', root]
    tests.run_decider(cmd, monkeypatch)

    outpath = os.path.join(root, 'decider__footnotes_user.yaml')
    assert os.path.exists(outpath), outpath

    dumped = utila.file_read(outpath)
    assert len(dumped) > 1000  # result contains some content
    assert '{%number%}' not in dumped, dumped  # ensure that template is replaced

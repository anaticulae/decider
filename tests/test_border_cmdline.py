# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import join

from utila import file_read
from utila import run_command

from border.cli import FEATURE_NAME
from border.cli import PROCESS_NAME
from border.cli import main
# pylint:disable=W0611
from tests.fixtures import rawmaker


def test_main(testdir, monkeypatch, rawmaker):  # # pylint:disable=W0621
    """Run decider with rawmaker_result to get hits output"""
    root = str(testdir)
    command = '-i %s -o %s -V --hitthebox' % (rawmaker, root)

    run_command(
        command,
        process=PROCESS_NAME,
        main=main,
        monkeypatch=monkeypatch,
        success=True,
    )

    outputfile = '%s__%s_hits.yaml' % (PROCESS_NAME, FEATURE_NAME)
    outputfile = join(root, outputfile)

    dumped = file_read(outputfile)
    assert len(dumped) > 100  # result contains some content

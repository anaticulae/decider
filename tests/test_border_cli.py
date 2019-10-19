# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import border.cli
# pylint:disable=W0611
from tests.fixtures import rawmaker


def test_cli_decider_border(testdir, monkeypatch, rawmaker):  # pylint:disable=W0621
    """Run decider with rawmaker_result to get hits output"""
    root = str(testdir)
    command = '-i %s -o %s -V --hitthebox' % (rawmaker, root)

    utila.run_command(
        command,
        process=border.cli.PROCESS,
        main=border.cli.main,
        monkeypatch=monkeypatch,
        success=True,
    )

    outputfile = f'{border.cli.PROCESS}__{border.cli.FEATURE_NAME}_hits.yaml'
    outputfile = os.path.join(root, outputfile)

    dumped = utila.file_read(outputfile)
    assert len(dumped) > 100  # result contains some content

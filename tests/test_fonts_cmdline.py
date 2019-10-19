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

import fonts.cli
# # pylint:disable=W0611
from tests.fixtures import rawmaker
from tests.resources import DECIDER_FONTS


def test_main_fonts(testdir, monkeypatch, rawmaker):  ## pylint:disable=W0621
    """Run decider with rawmaker_result to get hits output"""
    root = str(testdir)
    # copy ugly font config
    utila.copy_content(DECIDER_FONTS, root)
    utila.copy_content(rawmaker, root)

    command = ['-i', root, '-o', root]
    utila.run_command(
        command,
        process=fonts.cli.PROCESS,
        main=fonts.cli.main,
        monkeypatch=monkeypatch,
        success=True,
    )
    outpath = os.path.join(root, fonts.cli.UGLY_STEP_OUTPUT_FILE)
    assert os.path.exists(outpath), outpath

    dumped = utila.file_read(outpath)
    assert len(dumped) > 10  # result contains some content

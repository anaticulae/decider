# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import join

from utila import copy_content
from utila import file_read
from utila import run_command

from fonts.cli import PROCESS
from fonts.cli import main
# # pylint:disable=W0611
from tests.fixtures import rawmaker
from tests.resources import DECIDER_FONTS


def test_main_fonts(testdir, monkeypatch, rawmaker):  ## pylint:disable=W0621
    """Run decider with rawmaker_result to get hits output"""

    workspace = str(testdir)
    # copy ugly font config
    copy_content(DECIDER_FONTS, workspace)
    copy_content(rawmaker, workspace)

    command = ['-i', workspace, '-o', workspace]
    run_command(
        command,
        process=PROCESS,
        main=main,
        monkeypatch=monkeypatch,
        success=True,
    )
    outpath = join(workspace, 'decider_fonts__ugly_fonts.yaml')

    dumped = file_read(outpath)
    assert len(dumped) > 10  # result contains some content

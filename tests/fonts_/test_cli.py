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
import utila
import utilatest

import fonts.cli
import tests.resources


def test_main_fonts(testdir, monkeypatch):  ## pylint:disable=W0621
    """Run decider with rawmaker_result to get hits output"""
    root = str(testdir)
    # copy ugly font config
    utila.copy_content(tests.resources.DECIDER_FONTS, root)

    command = ['-i', power.link(power.DOCU35_PDF), '-o', root]
    utilatest.run_command(
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

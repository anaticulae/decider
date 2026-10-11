# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hoverpower
import utilo
import utilotest

import fonts.cli
import tests.resources


@utilotest.requires(hoverpower.DOCU035_PDF)
def test_main_fonts(td, mp):  # pylint:disable=W0621
    """Run decider with rawmaker_result to get hits output"""
    root = str(td)
    # copy ugly font config
    utilo.copy_content(tests.resources.DECIDER_FONTS, root)

    command = ['-i', hoverpower.link(hoverpower.DOCU035_PDF), '-o', root]
    utilotest.run_command(
        command,
        process=fonts.cli.PROCESS,
        main=fonts.cli.main,
        mp=mp,
        expect=True,
    )
    outpath = os.path.join(root, fonts.cli.UGLY_STEP_OUTPUT_FILE)
    assert os.path.exists(outpath), outpath

    dumped = utilo.file_read(outpath)
    assert len(dumped) > 10  # result contains some content

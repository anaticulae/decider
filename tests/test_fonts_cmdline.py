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

from fonts.cli import PROCESS_NAME
from fonts.cli import main
from tests import DECIDER_FONTS
from tests import RAWMAKER_RESULT


def test_main_fonts(testdir, monkeypatch):
    """Run decider with rawmaker_result to get hits output"""

    workspace = str(testdir)
    copy_content(DECIDER_FONTS, workspace)
    copy_content(RAWMAKER_RESULT, workspace)

    command = ['-i', workspace, '-o', workspace]
    run_command(
        command,
        process=PROCESS_NAME,
        main=main,
        monkeypatch=monkeypatch,
        success=True,
    )
    dumped = file_read(join(workspace, 'decider_fonts__ugly_fonts.yaml'))
    assert len(dumped) > 10  # result contains some content

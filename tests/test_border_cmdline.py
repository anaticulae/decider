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
from tests import RAWMAKER_RESULT


def test_main(testdir, monkeypatch):
    """Run decider with rawmaker_result to get hits output"""
    outputpath = str(testdir)
    command = ['-i', RAWMAKER_RESULT, '-o', outputpath, '-V', '--hitthebox']

    run_command(
        command,
        process=PROCESS_NAME,
        main=main,
        monkeypatch=monkeypatch,
        success=True,
    )
    outputfile = '%s__%s_hits.yaml' % (PROCESS_NAME, FEATURE_NAME)
    dumped = file_read(join(outputpath, outputfile))
    assert len(dumped) > 100  # result contains some content

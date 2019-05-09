# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from utila import SUCCESS
from utila import file_read

from border.command import PROCESS_NAME
from border.command import main
from tests import RAWMAKER_RESULT


def test_main(testdir, monkeypatch):
    """Run decider with rawmaker_result to get hits output"""
    outputpath = str(testdir)
    command = ['-i', RAWMAKER_RESULT, '-o', outputpath, '-V']
    result = None
    with monkeypatch.context() as context:
        context.setattr('sys.argv', [PROCESS_NAME] + command)
        result = main()
    assert result == SUCCESS, result
    dumped = file_read(outputpath + '/hitthebox__hits.yaml')
    assert len(dumped) > 100  # result contains some content

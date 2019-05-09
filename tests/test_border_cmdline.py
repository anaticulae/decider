# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from sys import argv

from utila import SUCCESS

from border.command import PROCESS_NAME
from border.command import main
from tests import RAWMAKER_RESULT


def test_main(testdir, monkeypatch):
    command = ['-i', RAWMAKER_RESULT, '-o', str(testdir), '-V']
    result = None
    with monkeypatch.context() as context:
        context.setattr('sys.argv', [PROCESS_NAME] + command)
        result = main()
        assert 0
    assert result == SUCCESS, result

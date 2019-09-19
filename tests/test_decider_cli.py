# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila

import decider


@pytest.mark.parametrize('cmd', [
    '--help',
])
def test_cli_decider(cmd, testdir, monkeypatch):
    """Run decider"""
    utila.run_command(
        cmd,
        process=decider.PROCESS,
        main=decider.cli.main,
        monkeypatch=monkeypatch,
        success=True,
    )

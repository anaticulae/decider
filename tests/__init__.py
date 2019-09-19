# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import decider


def run_decider(cmd: str, monkeypatch):
    utila.run_command(
        cmd,
        decider.PROCESS,
        decider.cli.main,
        success=True,
        monkeypatch=monkeypatch,
    )

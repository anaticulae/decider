# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.path
import iamraw
import serializeraw
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


def tableofcontent(path: str) -> iamraw.Toc:
    path = groupme.path.toc(path)
    result = serializeraw.load_toc(path)
    return result

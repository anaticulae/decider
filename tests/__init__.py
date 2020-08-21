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
import power
import protocol
import serializeraw
import utila
import utilatest

import decider
import tests.__patch__

power.setup(decider.ROOT)


def run_decider(cmd: str, monkeypatch) -> int:
    returncode = utilatest.run_command(
        cmd,
        decider.PROCESS,
        decider.cli.main,
        success=True,
        monkeypatch=monkeypatch,
    )
    return returncode


def tableofcontent(path: str) -> iamraw.Toc:
    path = groupme.path.toc(path)
    result = serializeraw.load_toc(path)
    return result


# TODO: MOVE TO PROTOCOL
def select(items, selected=None):
    if isinstance(selected, int):
        selected = [selected]
    content = [item.content for item in items]
    flatten = utila.flatten(content)
    ids = [item.msgid for item in flatten]
    if selected:
        ids = [item for item in ids if item in selected]
    return ids

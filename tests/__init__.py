# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import utila
import utilatest

import decider

power.setup(decider.ROOT)

run, fail = utilatest.create_cli_runner(decider)


def tableofcontent(path: str) -> iamraw.Toc:
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

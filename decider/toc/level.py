# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import collections

import iamraw


class TooFewChildren(collections.UserList):  # pylint:disable=too-many-ancestors
    pass


class LevelToDeep(collections.UserList):  # pylint:disable=too-many-ancestors
    pass


def validate_children(toc: iamraw.Toc) -> TooFewChildren:
    tofewchildren = TooFewChildren()

    def godown(item: iamraw.toc.TocLinkMixin):
        if len(item.children) == 1:
            # If subpoint has only one children, it is not a subpoint.
            tofewchildren.append(item)
        for children in item:
            godown(children)

    for item in toc:
        godown(item)
    return tofewchildren


def validate_deepness(toc: iamraw.Toc, maxdeep: int = 2) -> LevelToDeep:
    todeep = LevelToDeep()

    def godown(item: iamraw.toc.TocLinkMixin):
        if item.level > maxdeep:
            todeep.append(item)
        for children in item:
            godown(children)

    for item in toc:
        godown(item)
    return todeep

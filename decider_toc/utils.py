# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import iamraw
import iamraw.toc


class InvalidTocItems(collections.UserList):  # pylint:disable=too-many-ancestors
    pass


def flat(toc: iamraw.Toc):
    """Remove nested order and deliver a top down list of pages and
    sections."""
    result = []

    def godown(item: iamraw.toc.TocLinkMixin):
        result.append(item)
        for children in item:
            godown(children)

    for item in toc:
        godown(item)

    return result

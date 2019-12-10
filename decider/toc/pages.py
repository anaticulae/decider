# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Validate page order

Support:
    arabic numbers
    roman numbers

"""
import iamraw
import iamraw.toc


def validate(toc: iamraw.Toc):
    toc = flat(toc)
    for item in toc:
        print(item.page)
    result = []
    return result


def flat(toc: iamraw.Toc):
    result = []

    def godown(item: iamraw.toc.TocLinkMixin):
        result.append(item)
        for children in item:
            godown(children)

    for item in toc:
        godown(item)

    return result

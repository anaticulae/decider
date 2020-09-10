# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import iamraw.toc
import utila


def headlines_totoc(
        headlines: iamraw.PagesHeadlineList,
        remove_rawinfo: bool = False,
) -> 'iamraw.Toc':
    try:
        flat = utila.flatten(headlines)
    except TypeError:
        # list is already flat
        flat = headlines
    for item in flat:
        # TODO: THINK ABOUT THIS
        if item.level is None:
            item.level = 1
    result = iamraw.toc.create_toc(flat, remove_rawinfo=remove_rawinfo)
    return result


iamraw.headlines_totoc = headlines_totoc

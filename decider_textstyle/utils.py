# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import operator

import iamraw
import utila


def text_chunks(headlines, navigators) -> list:  # pylint:disable=R1260,W0613
    # TODO: SO BAD
    headlines = utila.flatten(headlines)

    visited = set()
    for headline in headlines:
        try:
            start, end = headline.container
        except TypeError:
            start, end = headline.container, headline.container
        for item in range(start, end + 1):
            visited.add((headline.page, item))

    flat = []
    for navigator in navigators:
        for index, line in enumerate(navigator):
            if (navigator.page, index) in visited:
                continue
            flat.append((navigator.page, index, line))

    for headline in headlines:
        try:
            position = (headline.page, headline.container[0])
        except TypeError:
            position = (headline.page, headline.container)
        flat.append((*position, headline))

    flat = sorted(flat, key=operator.itemgetter(0, 1))

    while flat and not isinstance(flat[0][2], iamraw.Headline):
        # sync to first headline
        flat = flat[1:]
    return flat


def page_chunks(items):
    if not items:
        return []
    result = []
    page = None
    for item in items:
        if item[0] != page:
            result.append([item[0], [item[2]]])
            page = item[0]
        else:
            result[-1][1].append(item[2])
    return result

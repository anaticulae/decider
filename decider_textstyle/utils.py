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
import serializeraw
import serializeraw.border
import serializeraw.headerfooter
import texmex
import utila


# TODO: REPLACE WITH IAMRAW CODE
def create_pagetextcontentnavigators_fromfile(
        text: str,
        textpositions: str,
        sizeandborderpath: str,
        headerfooterpath: str,
        fontheader: str = None,
        fontcontent: str = None,
        pages: tuple = None,
        mode=texmex.PageTextNavigatorMode.BOTH,
        *,
        fill_empty: bool = True,
        validate_leftright: bool = True,
):
    navigators = serializeraw.create_pagetextnavigators_fromfile(
        text,
        textpositions,
        fontheader,
        fontcontent,
        pages=pages,
        mode=mode,
        fill_empty=fill_empty,
    )

    headerfooter = serializeraw.headerfooter.load_headerfooter(
        headerfooterpath,
        pages=pages,
    )

    sizeandborder = serializeraw.border.load_pageborders(
        sizeandborderpath,
        pages=pages,
    )

    result = texmex.create_pagetextcontentnavigators(
        headerfooter=headerfooter,
        navigators=navigators,
        pages=pages,
        sizeandborder=sizeandborder,
        validate_leftright=validate_leftright,
    )
    return result


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

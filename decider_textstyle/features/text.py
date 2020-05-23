# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import operator
import typing

import doctextstyle.parser
import doctextstyle.serialize
import iamraw
import protocol
import serializeraw
import serializeraw.border
import serializeraw.headerfooter
import texmex
import utila


def work(  # pylint:disable=R0914
        textstyle: str,
        headlines: str,
        text: str,
        textpositions: str,
        sizeandborders: str,
        headerfooter: str,
        fontheader: str,
        fontcontent: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)

    expected = doctextstyle.serialize.load_docstyle(textstyle)
    headlines = serializeraw.load_headlines(headlines, pages=pages)

    fontstore = serializeraw.create_fontstore(
        fontheader,
        fontcontent,
        pages=pages,
    )
    navigators = create_pagetextcontentnavigators_fromfile(
        text=text,
        textpositions=textpositions,
        sizeandborderpath=sizeandborders,
        headerfooterpath=headerfooter,
        fontheader=fontheader,
        fontcontent=fontcontent,
        pages=pages,
    )

    if not headlines:
        utila.error('no headlines given')
    if not navigators:
        utila.error('no navigators given')

    if navigators and headlines:
        chunks = text_chunks(headlines, navigators, style=expected)
        data = protocol.driver(
            text_chunks=chunks,
            fontstore=fontstore,
            headlines=headlines,
            style=expected,
        )
        linting(data, linter)

    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(driver, linter: protocol.Linter):
    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
        )
        checker(call, driver)


SOLUTION_7550 = """\
Schriftgröße des Texts weicht ab

Die erkannte Schriftgröße **{%current%}** weicht von
der erwarteten Schriftgröße **{%expected%}**.
"""


def check_7550_check_text_size(linter: callable, driver):
    if not driver.style.text_size:
        return
    chunks = driver.text_chunks
    expected = driver.style.text_size
    for page, line, item in chunks:
        if isinstance(item, iamraw.Headline):
            continue

        textsize = item.style.textsize()
        if textsize == expected:
            continue

        location = protocol.RangedLocation(page=page, line=line)
        # TODO: CHECK FOR SINGLE CHAR OR WORDS TO BIG, BUT EXCLUDE HIGHNOTES
        linter(location=location, expected=expected, current=textsize)


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


def text_chunks(headlines, navigators, style) -> list:  # pylint:disable=R1260,W0613
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
